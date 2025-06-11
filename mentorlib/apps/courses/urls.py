from django.urls import path

from mentorlib.apps.courses import views

urlpatterns =[
    path("", views.index, name="index"),
    path("<int:id>/", views.course_details, name="course_details"),
    path("<int:id>/files/", views.course_files, name="course_files"),
    path("create", views.course_create, name="create"),
    path("ask", views.course_ask, name="ask")
]