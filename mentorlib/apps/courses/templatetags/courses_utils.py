from django import template
from mentorlib.apps.configuration.utils import get_resource_name

register = template.Library()


@register.filter('get_resource_name')
def get_resource(resource):
    return get_resource_name(resource)

@register.filter
def student_is_registered(course, user):
    return course.registered_students and len(course.registered_students.filter(student=user)) > 0 or False