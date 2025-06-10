from django import forms
from mentorlib.apps.configuration.models import Resource


class CourseFilterForm(forms.Form):
    resource = forms.ModelMultipleChoiceField(queryset=Resource.objects.all())
    mentor = forms.CharField(required=False)