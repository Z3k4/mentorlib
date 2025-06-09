from django.shortcuts import render
from mentorlib.apps.courses.models import Course

def index(request):
    return render(request, 'index.html', context={"courses":Course.objects.all()})
