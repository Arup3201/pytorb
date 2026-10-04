from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.utils.translation import gettext_lazy as _
from . import models

class RegisterForm(BaseUserCreationForm):

    class Meta(BaseUserCreationForm.Meta):
        model = models.User
        fields = ("email", "username", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "john@example.com"
        self.fields["email"].widget.attrs["required"] = True
        self.fields["email"].label = _("Email*")

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "john"

        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["placeholder"] = "John"
        self.fields["first_name"].label = _("First Name")

        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["placeholder"] = "Doe"
        self.fields["last_name"].label = _("Last Name")

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "****"

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "****"
        self.fields["password2"].label = _("Confirm Password")

class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "current-password"}),
    )

class AccountEditForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "skills")
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "skills": forms.TextInput(attrs={
                "class": "form-control"
            })
        }
        labels = {
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "skills": _("Skills"),
        }
        help_texts = {
            "skills": _("Enter multiple skills separated by commas.")
        }