from django import forms
from django.utils.translation import gettext_lazy as _
from . import models

class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = models.Project
        fields = ("title", "description", "topics")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "description": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "topics": forms.TextInput(attrs={
                "class": "form-control"
            })
        }
        labels = {
            "title": _("Title"),
            "description": _("Description"),
            "topics": _("Topics"),
        }
        help_texts = {
            "topics": _("Enter multiple topics separated by commas.")
        }