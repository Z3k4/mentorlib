from django.db import models
from mentorlib.apps.users.models import User, UserUpload
from datetime import datetime
from mentorlib.apps.configuration.models import Resource


class AskedCourse(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    duration = models.IntegerField()
    remote = models.BooleanField(default=False)
    date = models.DateTimeField()
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_date = models.DateTimeField()


class Course(models.Model):
    """Course model"""

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("Date created")
    duration = models.IntegerField("Course duration")
    remote = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    status = models.IntegerField(default=0)

    @property
    def available(self):
        return self.status != 2 and self.date > datetime.now()

    def __str__(self):
        return f"{self.resource} - {self.mentor}"


class CourseRegisteredStudent(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="registered_students"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registered_courses"
    )
    note = models.TextField(blank=True)


class Comments(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")


class CourseUploadFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="files")
    user_upload = models.ForeignKey(UserUpload, on_delete=models.CASCADE)
