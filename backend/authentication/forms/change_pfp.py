from django import forms

from authentication.models import User


class ChangePfpForm(forms.ModelForm):
    new_pfp = forms.ImageField(
        label="New profile picture", required=False, widget=forms.FileInput(
            attrs={"class": "form-input"}
        )
    )

    class Meta:
        model = User
        fields = ["new_pfp"]
