from django import forms


class SearchForm(forms.Form):
    search_query = forms.CharField(
        label="Query", widget=forms.TextInput(
            attrs={"class": "form_input"}
        )
    )
