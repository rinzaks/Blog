from django import forms
from adminpanel.models import Profile,Blog_Table,User,Comment_Table
from django.contrib.auth.forms import User,UserCreationForm
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields didn't match.")
        validate_password(password1, self.user)
        return password2

    def save(self):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        self.user.save()
        return self.user
    
class Registration_Form(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label='First Name',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    last_name = forms.CharField(
        required=True,
        label='Last Name',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
        )
    username = forms.CharField(
        label='User Name',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
        )
    password1 = forms.CharField(
        label='Password',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    password2 = forms.CharField(
        label='Confirm Password',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
    def clean_password(self):
        password1 = self.cleaned_data.get('password1')

        if(len('password1') < 8):
            return self.add_error('password1','Password should be atleast 8 didgits')
        if not re.search(r'[a-z]',password1):
            return self.add_error('password1','Password should have atleast 1 small letter')
        if not re.search(r'[A_Z]',password1):
            return self.add_error('password1','Password should have atleast 1 capital letter')
        if not re.search(r'[0-9]',password1):
            return self.add_error('password1','Password should have atleast 1 number')
        if not re.search(r'[!,@,#,$,%,&]',password1):
            return self.add_error('password1','Password should have atleast 1 special character')
    def clean(self):
        cleaned_data=super().clean()
        password = cleaned_data.get('password')
        password1 = cleaned_data.get('password1')
        if password and password1 and password != password1:
            self.add_error('password1','password donot match')
            return cleaned_data
class Login_Form(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    class Meta:
        model = User
        fields = ['username', 'password1']
class ProfileForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=20,
        label='Enter Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    profile_image = forms.ImageField(
        label='Profile Image',
        required=True
    )
    id_proof = forms.FileField(
        label='ID Proof',
        required=True
    )

    class Meta:
        model = Profile
        fields = ['phone', 'profile_image', 'id_proof']