from rest_framework.views import APIView
from rest_framework.response import Response
from mentorlib.apps.users.models import User, UserNote
from mentorlib.api.apps.users.serializers import UserSerializer, UserNotesSerializer


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