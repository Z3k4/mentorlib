from django import forms
from mentorlib.core.forms import StylizedForm
from django.core.validators import RegexValidator


class UserSettingsForm(StylizedForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    current_password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{8,}$",
                message="Le mot de passe ne respecte pas les critères",
                code="invalid_password",
            )
        ],
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{8,}$",
                message="Le mot de passe ne respecte pas les critères",
                code="invalid_password",
            )
        ],
    )


class RegisterPasswordForm(StylizedForm):
    email = forms.CharField(required=True)
    username = forms.CharField(required=True)
    firstname = forms.CharField(required=True)
    lastname = forms.CharField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            RegexValidator(
                regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&._-])[A-Za-z\d@$!%*?&._-]{8,}$",
                message="Le mot de passe ne respecte pas les critères",
                code="invalid_password",
            )
        ],
    )
