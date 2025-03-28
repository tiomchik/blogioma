from django import forms
from captcha.fields import CaptchaField

from authentication.models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30, min_length=4, label="Username", widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    email = forms.EmailField(
        max_length=320, required=False, label="Email (optional)",
        widget=forms.EmailInput(
            attrs={"class": "form-input"}
        )
    )

    password = forms.CharField(
        min_length=8, label="Password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    password1 = forms.CharField(
        min_length=8, label="Confirm password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    pfp = forms.ImageField(
        required=False, label="Profile picture (optional)",
        widget=forms.FileInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["username", "password", "password1"]
