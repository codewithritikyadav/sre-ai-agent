from django import forms
from .models import Incident


class IncidentForm(forms.ModelForm):

    class Meta:

        model = Incident

        fields = ['title', 'logs']

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter incident title'
                }
            ),

            'logs': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 10,
                    'placeholder': 'Paste logs here...'
                }
            )
        }