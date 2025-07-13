from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from mentorlib.apps.courses.models import (
    Course,
    AskedCourse,
    CourseRegisteredStudent,
    CourseUploadFile,
    Comment,
)
from mentorlib.apps.users.models import User, UserUpload
from mentorlib.apps.configuration.models import Resource
from django.views.decorators.csrf import requires_csrf_token
from datetime import datetime
from mentorlib.apps.courses.filters import CourseFilter
from mentorlib.apps.courses.forms import CourseFilterForm, CourseUploadForm
from mentorlib.core.utilities.file import handle_course_files
from django.http import HttpResponse
from mentorlib.settings import BASE_DIR
from pathlib import Path
from mentorlib.apps.users.utils import notify

NAV_URLS = {
    "course_nav": {
        "Informations": "courses:course_details",
        "Etudiant inscrits": "courses:course_students_registered",
        "Documents": "courses:course_files",
    },
}
CONTEXT = {**NAV_URLS, "messages": []}


def index(request):
    CONTEXT["courses"] = CourseFilter(request.GET, queryset=Course.objects.all())
    CONTEXT["filter_form"] = CourseFilterForm()

    for user in User.objects.all():
        notify(user)

    return render(request, "courses/index.html", context=CONTEXT)


def course_details(request, id):
    """Show basic course informations and handle comments messages"""
    course = Course.objects.get(id=id)
    CONTEXT["course"] = course

    action = request.GET.get("action")

    if not request.user.is_anonymous:
        if action:
            course_registered = CourseRegisteredStudent.objects.filter(
                student=request.user, course=course
            ).first()
            if action == "unsuscribe":
                if course_registered:
                    course_registered.delete()
                    CONTEXT["messages"].append(
                        {"color": "red", "text": "Vous vous êtes désinscrit"}
                    )
                else:
                    CONTEXT["messages"].append(
                        {"color": "red", "text": "Vous n'êtes pas inscrit"}
                    )
            elif action == "suscribe" and not course_registered:
                course_registered = CourseRegisteredStudent(
                    student=request.user, course=course
                )
                course_registered.save()
                CONTEXT["messages"].append(
                    {
                        "color": "green",
                        "text": "Votre inscription a bien été prit en compte",
                    }
                )

        if request.method == "POST" and request.POST.get("message"):
            comment = Comment(
                course=Course.objects.get(id=id),
                comment=request.POST.get("message"),
                user=request.user,
            )

            comment.save()

    return render(request, "courses/tabs/informations.html", context=CONTEXT)


def duration_to_minutes(duration: str):
    duration_split = duration.split(":")
    return int(duration_split[0]) * 60 + int(duration_split[1])


@login_required(redirect_field_name="my_redirect_field")
@requires_csrf_token
def course_create(request):
    if request.method == "POST":
        convert_date = datetime.strptime(
            f"{request.POST['date']} {request.POST['time']}", "%m/%d/%Y %H:%M"
        )
        course = Course(
            mentor=User.objects.get(id=request.user.id),
            resource=Resource.objects.get(id=request.POST["resource"]),
            date=convert_date,
            duration=duration_to_minutes(request.POST["duration"]),
        )

        course.save()

        if course:
            return render(request, "courses/action_success.html")

    resources = Resource.objects.all()
    return render(request, "courses/create.html", context={"resources": resources})


@requires_csrf_token
def course_ask(request):
    if not request.user.is_authenticated:
        return redirect("/users/login")

    if request.method == "POST":
        convert_date = datetime.strptime(
            f"{request.POST['date']} {request.POST['time']}", "%m/%d/%Y %H:%M"
        )
        course = AskedCourse(
            student=User.objects.get(id=request.user.id),
            resource=Resource.objects.get(id=request.POST["resource"]),
            date=convert_date,
            duration=duration_to_minutes(request.POST["duration"]),
        )

        course.save()

        if course:
            return render(request, "courses/action_success.html")

    resources = Resource.objects.all()
    return render(request, "courses/ask.html", context={"resources": resources})


@requires_csrf_token
def course_files(request, id):
    course = Course.objects.get(id=id)
    CONTEXT["form"] = CourseUploadForm()
    CONTEXT["course"] = course

    if request.method == "POST":
        handle_course_files(course, request.user, request.FILES["file"])

    return render(request, "courses/tabs/documents.html", context=CONTEXT)


def course_views_file(request, id, file_id):
    course_upload_file = CourseUploadFile.objects.get(
        course=Course.objects.get(id=id), user_upload=UserUpload.objects.get(id=file_id)
    )
    path = Path(BASE_DIR) / course_upload_file.user_upload.file_path
    image_data = open(path, "rb").read()

    return HttpResponse(
        image_data, content_type=course_upload_file.user_upload.metadata["content_type"]
    )


@requires_csrf_token
def course_students_registered(request, id):
    course = Course.objects.get(id=id)
    CONTEXT["course"] = course

    if request.method == "POST" and request.POST.get("student_note"):
        course_registered = CourseRegisteredStudent.objects.get(
            student=request.user, course=course
        )
        course_registered.note = request.POST.get("student_note")
        course_registered.save()

    return render(request, "courses/tabs/register_informations.html", context=CONTEXT)
