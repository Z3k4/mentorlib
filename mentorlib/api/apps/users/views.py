from rest_framework.views import APIView
from rest_framework.response import Response
from mentorlib.apps.users.models import User, UserNote, Notification, NotificationType
from mentorlib.api.apps.users.serializers import (
    UserSerializer,
    UserNotesSerializer,
    NotificationSerializer,
)
from mentorlib.apps.users.utils import notify


class UserView(APIView):
    def get(self, request, user_id):
        items = User.objects.get(id=user_id)
        serializer = UserSerializer(items, many=False)
        return Response(serializer.data)


class UserNotesView(APIView):
    def get(self, request, user_id):
        items = UserNote.objects.filter(user=user_id)
        serializer = UserNotesSerializer(items, many=True)

        return Response(serializer.data)


class AllUsersView(APIView):
    def get(self, request):
        items = User.objects.all()
        serializer = UserSerializer(items, many=True)
        return Response(serializer.data)


class AllUsersNotesView(APIView):
    def get(self, request):
        items = UserNote.objects.filter()
        serializer = UserNotesSerializer(items, many=True)

        return Response(serializer.data)


class NotificationView(APIView):
    def get(self, request):
        items = Notification.objects.filter(user=request.user.id)
        serializer = NotificationSerializer(items, many=True)

        notification_type = NotificationType.objects.get(short_name="course_comment")
        variables = {"comment": "ok"}
        notify(User.objects.get(id=1), notification_type, variables)

        return Response(serializer.data)
