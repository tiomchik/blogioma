from django import forms
from captcha.fields import CaptchaField

from authentication.models import User


class ChangeUsernameForm(forms.ModelForm):
    new_username = forms.CharField(
        max_length=30, min_length=4, label="New username",
        widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["new_username"]
