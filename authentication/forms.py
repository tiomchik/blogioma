from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import Profile


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
        model = Profile
        fields = ["username", "password", "password1"]


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, min_length=4, label="Username", widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    password = forms.CharField(
        min_length=8, label="Password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()


class ChangeUsernameForm(forms.ModelForm):
    new_username = forms.CharField(
        max_length=30, min_length=4, label="New username",
        widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()

    class Meta:
        model = Profile
        fields = ["new_username"]


class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(
        min_length=8, label="New password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    new_password1 = forms.CharField(
        min_length=8, label="Confrim new password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["new_password", "new_password1"]


class ChangePfpForm(forms.ModelForm):
    new_pfp = forms.ImageField(
        label="New profile picture", required=False, widget=forms.FileInput(
            attrs={"class": "form-input"}
        )
    )

    class Meta:
        model = Profile
        fields = ["new_pfp"]
