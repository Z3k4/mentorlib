from django import forms
from mentorlib.core.forms import StylizedForm


class UserSettingsForm(StylizedForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    current_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
