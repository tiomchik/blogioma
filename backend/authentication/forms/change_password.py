from django import forms
from captcha.fields import CaptchaField

from authentication.models import User


class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(
        min_length=8, label="New password", widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    new_password1 = forms.CharField(
        min_length=8, label="Confirm new password",
        widget=forms.PasswordInput(
            attrs={"class": "form-input"}
        )
    )

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ["new_password", "new_password1"]
