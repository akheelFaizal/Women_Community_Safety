from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Optional'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone_number')
