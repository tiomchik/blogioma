from django import forms


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
