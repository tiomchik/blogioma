from django import forms
from captcha.fields import CaptchaField


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
