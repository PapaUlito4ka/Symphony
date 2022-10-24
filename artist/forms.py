from django.forms import Form, EmailField, CharField, PasswordInput, TextInput
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from artist.models import Artist


class SignUpForm(Form):
    email = EmailField(max_length=128)
    name = CharField(max_length=128)
    password = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    password_confirm = CharField(
        label=_("Password confirm"),
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "email_already_exists": _(
            "Email already exists"
        ),
        "passwords_mismatch": _(
            "Provided passwords didn't match"
        ),
    }

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if email and password and password_confirm:
            if password != password_confirm:
                raise self.passwords_mismatch()
            if Artist.objects.filter(email=email).exists():
                raise self.email_already_exists()

        return self.cleaned_data

    def email_already_exists(self):
        return ValidationError(
            self.error_messages["email_already_exists"],
            code="email_already_exists",
        )

    def passwords_mismatch(self):
        return ValidationError(
            self.error_messages["passwords_mismatch"],
            code="passwords_mismatch",
        )
