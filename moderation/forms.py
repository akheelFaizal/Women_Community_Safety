from django import forms
from reports.models import ReportResponse
from awareness.models import Post

class ReportResponseForm(forms.ModelForm):
    class Meta:
        model = ReportResponse
        fields = ['message', 'is_internal']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'is_internal': 'Internal Note Only (Not visible to user)'
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class SafetyFeedForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alert Headline'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Details of the safety alert...'}),
        }
