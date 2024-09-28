from django import forms
from .models import User

class Login_Form(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    class Meta:
        model = User
        fields = ['username', 'password1']