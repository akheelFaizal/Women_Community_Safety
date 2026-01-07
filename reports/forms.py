from django import forms
from .models import Report, ReportAttachment

class ReportForm(forms.ModelForm):
    attachment = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}), label="Upload Evidence (Optional)")

    class Meta:
        model = Report
        fields = ['category', 'description', 'location_text', 'is_anonymous']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the incident...'}),
            'location_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where did this happen?'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'location_text': 'Location',
            'is_anonymous': 'Submit Anonymously'
        }
