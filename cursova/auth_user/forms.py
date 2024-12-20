from django.contrib.auth.forms import UserCreationForm
from django import forms

from auth_user.models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["fullname", "email", "phone", "password1", "password2"]

#login form
class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

