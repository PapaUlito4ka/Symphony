from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from artist.forms import SignUpForm


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'admin/sign_up.html'
    success_url = reverse_lazy('admin:login')
