from django.db import models
from mentorlib.apps.courses.templatetags.courses_utils import get_resource_name

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class StudyYear(models.Model):

    order = models.IntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Semester(models.Model):

    order = models.IntegerField()
    semester = models.IntegerField()

    year = models.ForeignKey(StudyYear, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.year} - S{self.semester}"

class Resource(models.Model):

    number = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    banner = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{get_resource_name(self)} {self.name}"