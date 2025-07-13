from django.shortcuts import render
from mentorlib.apps.courses.models import Course
from mentorlib.apps.users.utils import notify
from mentorlib.apps.users.models import User


def index(request):
    for user in User.objects.all():
        notify(user)

    return render(request, "index.html", context={"courses": Course.objects.all()})
