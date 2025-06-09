from django import template
from mentorlib.apps.users.models import User

register = template.Library()

@register.filter
def get_size(value):
    return 'xs' if value == 'lower' else 'base'

@register.filter('get_initial_letter')
def get_initial_letter(user:User):
    return user.first_name[:1].upper() + user.last_name[:1].upper() or "UU"

@register.filter
def get_fullname(user:User):
    return f"{(user.first_name or 'Unknown')} {(user.last_name) or 'Unknown'}"