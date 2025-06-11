from django.contrib import admin
from mentorlib.apps.configuration.models import (
    Resource,
    StudyYear,
    Semester,
    Department,
)
from mentorlib.apps.users.models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Resource)
admin.site.register(StudyYear)
admin.site.register(Semester)
admin.site.register(Department)
admin.site.register(User, UserAdmin)
