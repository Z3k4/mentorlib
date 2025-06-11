from rest_framework import serializers
from mentorlib.apps.users.models import User, UserNote
from mentorlib.api.apps.configuration.serializers import ResourceSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "is_active")


class UserNotesSerializer(serializers.ModelSerializer):
    mentor = UserSerializer()
    user = UserSerializer()
    resource = ResourceSerializer()

    class Meta:
        model = UserNote
        fields = "__all__"
