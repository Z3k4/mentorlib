from django.shortcuts import render
from mentorlib.apps.courses.models import Course, AskedCourse, CourseRegisteredStudent
from mentorlib.apps.users.utils import can_mentor
from datetime import datetime

NAV_URLS = {
    "mentor_nav": {"Vos cours": "mentor_mentoring", "En attente": "mentor_awaiting"},
    "student_nav": {"Suivis": "student_following", "En attente": "student_asked"},
}

CONTEXT = {**NAV_URLS}


def student_space_following(request):
    courses_followed = request.user.registered_courses.select_related()
    CONTEXT["courses_followed"] = courses_followed
    return render(request, "spaces/student/following.html", context=CONTEXT)


def student_space_asked(request):
    courses_asked = AskedCourse.objects.filter(approved_date=None, student=request.user)
    CONTEXT["courses_asked"] = courses_asked

    return render(request, "spaces/student/asked.html", context=CONTEXT)


def mentor_space_mentoring(request):
    courses_mentored = Course.objects.filter(mentor_id=request.user.id)
    CONTEXT["courses_mentored"] = courses_mentored
    return render(request, "spaces/mentor/mentoring.html", context=CONTEXT)


def mentor_space_awaiting(request):
    courses_awaiting = AskedCourse.objects.filter(approved_date=None)
    CONTEXT["courses_awaiting"] = courses_awaiting

    action = request.GET.get("action")
    if action:
        id = request.GET.get("id")
        asked_course = AskedCourse.objects.get(id=id, approved_date=None)

        if can_mentor(request.user, asked_course.resource):
            new_course = Course(
                mentor=request.user,
                resource=asked_course.resource,
                date=asked_course.date,
                duration=asked_course.duration,
            )

            new_course.save()

            # Register student

            course_registered = CourseRegisteredStudent(
                student=asked_course.student, course=new_course
            )
            course_registered.save()

            asked_course.approved_date = datetime.now()
            asked_course.save()

    return render(request, "spaces/mentor/awaiting.html", context=CONTEXT)
