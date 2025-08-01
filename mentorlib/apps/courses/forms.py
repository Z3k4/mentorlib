from django import forms
from mentorlib.core.forms import StylizedForm
from mentorlib.apps.configuration.models import Resource
from mentorlib.apps.users.validators import FileValidator


class CourseFilterForm(StylizedForm):
    resource = forms.ModelMultipleChoiceField(queryset=Resource.objects.all())
    mentor = forms.CharField(required=False)


class CourseUploadForm(StylizedForm):
    file = forms.FileField(widget=forms.FileInput, validators=[FileValidator(["pdf"])])
