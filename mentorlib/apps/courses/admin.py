from django.contrib import admin
# Register your models here.
from mentorlib.apps.courses.models import Course

class CourseAdmin(admin.ModelAdmin):
    save_as=True

admin.site.register(Course, CourseAdmin)