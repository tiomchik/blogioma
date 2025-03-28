from django import forms

from feedback.models import Report


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
