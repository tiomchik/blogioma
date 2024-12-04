from django import forms

from .models import Report


class FeedbackForm(forms.Form):
    email = forms.EmailField(
        max_length=320, required=False, label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-input"}
        )
    )

    problem = forms.CharField(
        min_length=5, max_length=50, label="Heading", widget=forms.TextInput(
            attrs={"class": "form-input"}
        )
    )

    problem_desc = forms.CharField(
        min_length=10, max_length=500, label="Describe the problem",
        widget=forms.Textarea(
            attrs={"class": "form-textarea"}
        )
    )


class ReportForm(forms.ModelForm):
    desc = forms.CharField(
        max_length=200, label="Describe the infringement (optional)",
        required=False, widget=forms.Textarea(
            attrs={"class": "form-textarea"}
        )
    )

    class Meta:
        model = Report
        fields = ["reason", "desc"]
