from django.urls import path

from mentorlib.apps.spaces import views

urlpatterns = [
    path("student/following/", views.student_space_following, name="student_following"),
    path("student/asked/", views.student_space_asked, name="student_asked"),
    path("mentor/mentoring/", views.mentor_space_mentoring, name="mentor_mentoring"),
    path("mentor/awaiting/", views.mentor_space_awaiting, name="mentor_awaiting"),
]
