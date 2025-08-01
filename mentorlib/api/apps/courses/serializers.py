from rest_framework import serializers
from mentorlib.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ("password", "is_active")
