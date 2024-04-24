from django import forms

from .models import Article


class AddArticleForm(forms.ModelForm):
    headling = forms.CharField(
        min_length=4, max_length=32, label="Headling", widget=forms.TextInput(
            attrs={"class": "form_input"}
        )
    )

    full_text = forms.CharField(
        min_length=1, label="Text", widget=forms.Textarea(
            attrs={"class": "form_textarea"}
        )
    )

    class Meta:
        model = Article
        fields = ["headling", "full_text"]
