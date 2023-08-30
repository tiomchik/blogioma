from django import forms
from .models import *

from captcha.fields import CaptchaField


class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=30, min_length=4, label="Username", widget=forms.TextInput(
        attrs={"class": "form_input"}
    ))

    email = forms.EmailField(max_length=320, required=False, label="Email (optional)", widget=forms.EmailInput(
        attrs={"class": "form_input"}
    ))

    password = forms.CharField(min_length=8, label="Password", widget=forms.PasswordInput(
        attrs={"class": "form_input"}
    ))

    password1 = forms.CharField(min_length=8, label="Confirm password", widget=forms.PasswordInput(
        attrs={"class": "form_input"}
    ))

    pfp = forms.ImageField(required=False, 
                label="Profile picture (optional)", widget=forms.FileInput(
                    attrs={"class": "form_input"}
                ))

    captcha = CaptchaField()

    class Meta:
        model = Profile
        fields = ["username", "password", "password1"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=4, label="Username", widget=forms.TextInput(
        attrs={"class": "form_input"}
    ))

    password = forms.CharField(min_length=8, label="Password", widget=forms.PasswordInput(
        attrs={"class": "form_input"}
    ))

    captcha = CaptchaField()


class AddArticleForm(forms.ModelForm):
    headling = forms.CharField(min_length=4, max_length=32, label="Headling", widget=forms.TextInput(
        attrs={"class": "form_input"}
    ))

    full_text = forms.CharField(min_length=1, label="Text", widget=forms.Textarea(
        attrs={"class": "form_textarea"}
    ))

    class Meta:
        model = Article
        fields = ["headling", "full_text"]


class AddCommentForm(forms.ModelForm):
    text = forms.CharField(min_length=10, max_length=400,
            label="Comment", widget=forms.Textarea(
                attrs={"class": "form_textarea"}
            ))

    class Meta:
        model = Comment
        fields = ["text"]


class SearchForm(forms.Form):
    search_query = forms.CharField(label="Query", 
            widget=forms.TextInput(
                attrs={"class": "form_input"}
            ))


class ChangeUsernameForm(forms.ModelForm):
    new_username = forms.CharField(max_length=30, min_length=4,
    label="New username", widget=forms.TextInput(
                                    attrs={"class": "form_input"}
                                ))
    
    captcha = CaptchaField()
    
    class Meta:
        model = Profile
        fields = ["new_username"]


class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(min_length=8, 
                label="New password", 
        widget=forms.PasswordInput(
            attrs={"class": "form_input"}
        ))
    
    new_password1 = forms.CharField(min_length=8, 
                label="Confrim new password", 
        widget=forms.PasswordInput(
            attrs={"class": "form_input"}
        ))
    
    captcha = CaptchaField()
    
    class Meta:
        model = User
        fields = ["new_password", "new_password1"]


class ChangePfpForm(forms.ModelForm):
    new_pfp = forms.ImageField(label="New profile picture", 
            required=False,
            widget=forms.FileInput(
                attrs={"class": "form_input"}
            ))
    
    class Meta:
        model = Profile
        fields = ["new_pfp"]


class FeedbackForm(forms.Form):
    email = forms.EmailField(max_length=320, required=False,
        label="Email", widget=forms.EmailInput(
                        attrs={"class": "form_input"}
                    ))

    problem = forms.CharField(min_length=5, max_length=50, 
                label="Headling", widget=forms.TextInput(
                        attrs={"class": "form_input"}
                    ))
    
    problem_desc = forms.CharField(min_length=10, max_length=500, 
        label="Describe the problem", widget=forms.Textarea(
                        attrs={"class": "form_textarea"}
                    ))


class ReportForm(forms.ModelForm):
    desc = forms.CharField(max_length=200, 
        label="Describe the infringement (optional)", 
        required=False, widget=forms.Textarea(
                            attrs={"class": "form_textarea"}
                        ))

    class Meta:
        model = Report
        fields = ["reason", "desc"]
