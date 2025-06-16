from mentorlib.apps.users.models import User
from mentorlib.apps.configuration.models import Resource


def can_mentor(user: User, resource: Resource):
    if user.has_perm("users.super_mentoring"):
        return True

    if user.semester == resource.semester or (
        user.semester and user.semester.is_after(resource.semester)
    ):
        return True

    return False
