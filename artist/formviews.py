from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db import transaction

from artist.forms import SignUpForm
from artist.models import Artist, ArtistProfile, Album, Song


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'admin/sign_up.html'
    success_url = reverse_lazy('admin:login')

    @transaction.atomic
    def form_valid(self, form: SignUpForm):
        artist = Artist.objects.create(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password'),
        )
        ArtistProfile.objects.create(
            artist=artist,
            name=form.cleaned_data.get('name')
        )
        content_types = [v for _, v in ContentType.objects.get_for_models(Album, ArtistProfile, Song).items()]
        permissions = Permission.objects.filter(content_type__in=content_types)
        artist.user_permissions.add(*permissions)
        return super(SignUpView, self).form_valid(form)
