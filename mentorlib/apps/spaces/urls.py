from django.urls import path

from mentorlib.apps.spaces import views

urlpatterns =[
    path("student", views.student_space, name="student"),
    path("mentor", views.mentor_space, name="mentor")
]