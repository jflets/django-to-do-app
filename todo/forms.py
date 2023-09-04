from django import forms
from .models import item


class itemForm(forms.ModelForm):
    class Meta:
        model = item
        fields = ['name', 'done']
