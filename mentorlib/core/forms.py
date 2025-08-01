from django import forms
from django.forms.renderers import TemplatesSetting


class StylizedForm(forms.Form):
    template_name = "components/form_render.html"
    default_renderer = TemplatesSetting()
