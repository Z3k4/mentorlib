from django import forms
from mentorlib.apps.configuration.models import Resource
from mentorlib.settings import BASE_DIR

class CourseFilterForm(forms.Form):
    resource = forms.ModelMultipleChoiceField(queryset=Resource.objects.all())
    mentor = forms.CharField(required=False)

class CourseUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput)