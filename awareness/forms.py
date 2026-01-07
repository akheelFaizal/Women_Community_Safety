from django import forms
from .models import EmergencyContact

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'number', 'description', 'priority']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Women Helpline'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1091'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief description'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0-100 (higher = top)'}),
        }
