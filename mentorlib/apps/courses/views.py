from django.shortcuts import render, redirect
from mentorlib.apps.courses.models import Course, AskedCourse, CourseRegisteredStudent
from mentorlib.apps.users.models import User
from mentorlib.apps.configuration.models import Resource
from django.views.decorators.csrf import requires_csrf_token
from datetime import datetime
from mentorlib.apps.courses.filters import CourseFilter
from mentorlib.apps.courses.forms import CourseFilterForm, CourseUploadForm
from mentorlib.core.utilities.file import handle_course_files

def index(request):
    context = {}
    context['courses'] = CourseFilter(request.GET, queryset=Course.objects.all())
    context["filter_form"] = CourseFilterForm()
    return render(request, 'courses/index.html', context=context)

def course_details(request, id):
    course = Course.objects.get(id=id)
    context = {
        "messages":[],
        "course":course,
        "file_upload":CourseUploadForm()
    }
    action = request.GET.get("action")

    if action:
        course_registered = CourseRegisteredStudent.objects.filter(student=request.user, course=course).first()
        if action == "unsuscribe":
            if course_registered:
                course_registered.delete()
                context["messages"].append({"color":"red","text":"Vous vous êtes désinscrit"})
            else:
                context["messages"].append({"color":"red","text":"Vous n'êtes pas inscrit"})
        elif action =="suscribe" and not course_registered:
            course_registered = CourseRegisteredStudent(student=request.user, course=course)
            course_registered.save()
            context["messages"].append({"color":"green","text":"Votre inscription a bien été prit en compte"})

    if request.method == "POST" and request.POST.get('student_note'):
        course_registered = CourseRegisteredStudent.objects.get(student=request.user, course=course)
        course_registered.note = request.POST.get("student_note")
        course_registered.save()

    return render(request, 'courses/details.html', context=context)

def duration_to_minutes(duration:str):
    duration_split = duration.split(":")
    return int(duration_split[0]) * 60 + int(duration_split[1])

@requires_csrf_token
def course_create(request):
    context = {
        "message":[]
    }
    if not request.user.is_authenticated:
        return redirect("/users/login")

    if request.method == "POST":
        convert_date = datetime.strptime(f"{request.POST['date']} {request.POST['time']}", "%m/%d/%Y %H:%M")
        course = Course(
            mentor=User.objects.get(id=request.user.id),
            resource=Resource.objects.get(id=request.POST['resource']),
            date=convert_date,
            duration=duration_to_minutes(request.POST['duration'])
        )

        course.save()

        if course:
            return render(request, 'courses/action_success.html')
    
    resources = Resource.objects.all()
    return render(request, 'courses/create.html', context={"resources":resources})

@requires_csrf_token
def course_ask(request):
    if not request.user.is_authenticated:
        return redirect("/users/login")

    if request.method == "POST":
        convert_date = datetime.strptime(f"{request.POST['date']} {request.POST['time']}", "%m/%d/%Y %H:%M")
        course = AskedCourse(
            mentor=User.objects.get(id=request.user.id),
            resource=Resource.objects.get(id=request.POST['resource']),
            date=convert_date,
            duration=duration_to_minutes(request.POST['duration'])
        )

        course.save()

        if course:
            return render(request, 'courses/action_success.html')
    
    resources = Resource.objects.all()
    return render(request, 'courses/ask.html', context={"resources":resources})
    

@requires_csrf_token
def course_files(request, id):
    course = Course.objects.get(id=id)
    handle_course_files(course, request.POST['file'])

    return course_details(request, id)