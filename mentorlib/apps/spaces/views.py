from django.shortcuts import render
from mentorlib.apps.courses.models import Course

def student_space(request):
    courses_followed = request.user.registered_courses.select_related()
    return render(request, 'spaces/student.html', context={'courses_followed':courses_followed})

def mentor_space(request):
    courses_mentored = Course.objects.filter(mentor_id=request.user.id)
    return render(request, 'spaces/mentor.html', context={'courses_mentored':courses_mentored})