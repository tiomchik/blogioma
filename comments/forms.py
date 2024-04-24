from django import forms

from .models import Comment


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(
        min_length=10, max_length=400, label="Comment", widget=forms.Textarea(
            attrs={"class": "form_textarea"}
        )
    )

    class Meta:
        model = Comment
        fields = ["text"]
