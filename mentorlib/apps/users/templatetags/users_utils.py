from django import template
from mentorlib.apps.users.models import User, UserUpload

register = template.Library()


@register.filter
def get_size(value):
    return "xs" if value == "lower" else "base"


@register.filter("get_initial_letter")
def get_initial_letter(user: User):
    return user.first_name[:1].upper() + user.last_name[:1].upper() or "UU"


@register.filter
def get_fullname(user: User):
    return f"{(user.first_name or 'Unknown')} {(user.last_name) or 'Unknown'}"


@register.filter
def get_file_size(file: UserUpload):
    SIZE_LABELS = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}
    file_size = int(file.metadata["size"])
    size = [
        f"{round(file_size / SIZE_LABELS[label], 2)} {label}"
        for label in SIZE_LABELS
        if not (file_size / SIZE_LABELS[label]) > 1024
        and (file_size / SIZE_LABELS[label]) > 1
    ]
    return size[-1] if size else f"{file_size} BYTES"
