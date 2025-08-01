from django.urls import path

from mentorlib.apps.courses import views

app_name = "courses"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/", views.course_details, name="course_details"),
    path("<int:id>/files/", views.course_files, name="course_files"),
    path(
        "<int:id>/files/<int:file_id>",
        views.course_views_file,
        name="course_view_files",
    ),
    path(
        "<int:id>/registered/",
        views.course_students_registered,
        name="course_students_registered",
    ),
    path("create", views.course_create, name="create"),
    path("ask", views.course_ask, name="ask"),
]
