from django.db import models
from django.contrib.auth.models import AbstractUser
from mentorlib.apps.configuration.models import Resource, Semester, StudyYear
from datetime import datetime
from pathlib import Path
from mentorlib.settings import UPLOADS_DIR, BASE_DIR


class User(AbstractUser):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(blank=True, null=True)
    semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, default=None, null=True
    )
    study_year = models.ForeignKey(
        StudyYear, on_delete=models.SET_NULL, default=None, null=True
    )

    class Meta:
        permissions = [
            ("mentoring", "Allow mentoring for user"),
            (
                "super_mentoring",
                "Allow mentoring for user even his year is under the resource",
            ),
        ]

    @property
    def notifications(self):
        return Notification.objects.filter(user=self, readed=False)

    def get_full_name(self):
        return f"{(self.last_name or 'Unknown')} {(self.first_name or 'Unknown')}"

    def __str__(self):
        return f"{self.username}"


class UserNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.id} Student<{self.user.username}>Mentor<{self.mentor.username}>"


class UploadMetadata(models.Model):
    NAME = "name"
    EXTENSION = "extension"
    SIZE = "size"
    PAGES = "pages"
    CONTENT_TYPE = "content_type"

    METADATA_TYPE_CHOICE = {
        NAME: "Name",
        EXTENSION: "Extension",
        SIZE: "Size",
        PAGES: "Pages",
        CONTENT_TYPE: "ContentType",
    }
    name = models.CharField(
        choices=METADATA_TYPE_CHOICE,
    )
    value = models.CharField()
    user_upload = models.ForeignKey("UserUpload", on_delete=models.CASCADE)


class UserUpload(models.Model):
    """UserUpload model"""

    file_path = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploads")
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        permissions = [("upload_files", "Can upload files")]

    @property
    def metadata(self):
        return {
            meta.name: meta.value
            for meta in UploadMetadata.objects.filter(user_upload=self)
        }

    @property
    def absolute_path(self):
        return Path(BASE_DIR) / UPLOADS_DIR / self.file_path

    def erase(self):
        file = Path(self.absolute_path)

        if file.exists():
            file.unlink()

    def __str__(self):
        return f"{self.file_path}"


class NotificationType(models.Model):
    short_name = models.CharField(max_length=100, unique=True, default="")
    text = models.CharField(max_length=255)
    link = models.CharField()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(
        NotificationType, on_delete=models.CASCADE, related_name="notifications"
    )
    readed = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now)
    variables = models.JSONField()

    @property
    def text(self):
        return self.type.text % self.variables
