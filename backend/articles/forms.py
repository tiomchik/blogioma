from django import forms

from .models import Article


class AddArticleForm(forms.ModelForm):
    heading = forms.CharField(
        min_length=1, max_length=100, label="Heading", widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    full_text = forms.CharField(
        min_length=1, label="Text", widget=forms.Textarea(
            attrs={"class": "form-textarea"}
        )
    )

    class Meta:
        model = Article
        fields = ["heading", "full_text"]
