from django import forms

from .models import Article


class AddArticleForm(forms.ModelForm):
    headling = forms.CharField(
        min_length=1, max_length=100, label="Headling", widget=forms.TextInput(
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
        fields = ["headling", "full_text"]
