from django import forms
from django.utils.translation import gettext_lazy as _
from . import models

class TaskForm(forms.ModelForm):

    class Meta:
        model = models.Task
        fields = ("title", "description", "status")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control"
            }),
            "status": forms.Select(attrs={
                "class": "form-control"
            })
        }
        labels = {
            "title": _("Title"),
            "description": _("Description"),
            "status": _("Status"),
        }
