from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.db import transaction

from artist.forms import SignUpForm
from artist.models import Artist, ArtistProfile
from artist.permissions import artist_permissions


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
        artist.user_permissions.add(*artist_permissions())
        return super(SignUpView, self).form_valid(form)
