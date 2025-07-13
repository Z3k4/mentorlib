from mentorlib.apps.users.models import User, Notification, NotificationType
from mentorlib.apps.configuration.models import Resource
from mentorlib.apps.courses.models import Course
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from mentorlib.api.apps.users.serializers import NotificationSerializer


def can_mentor(user: User, resource: Resource):
    if user.has_perm("users.super_mentoring"):
        return True

    if user.semester == resource.semester or (
        user.semester and user.semester.is_after(resource.semester)
    ):
        return True

    return False


def notify(
    user: User, notification_type: NotificationType = None, json_variables: str = None
):
    if notification_type and json_variables:
        notification = Notification(
            type=notification_type, variables=json_variables, user=user
        )

        notification.save()

        serialized_notification = NotificationSerializer(notification, many=False)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {"type": "notify", "content": {**serialized_notification.data}},
        )


def notify_users_related_to_course(
    course: Course,
    notification_type: NotificationType,
    json_variables: str,
    excludes_id=[],
):
    for (
        course_registered_student
    ) in course.registered_students.select_related().exclude(
        student_id__in=excludes_id
    ):
        notify(course_registered_student.student, notification_type, json_variables)

    if course.mentor.id not in excludes_id:
        notify(course.mentor, notification_type, json_variables)
