from django.db import models
from django.contrib.auth.models import AbstractUser
from mentorlib.apps.configuration.models import Resource
from datetime import datetime

class User(AbstractUser):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.username}"


class UserNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    date = models.DateTimeField(default=datetime.now)