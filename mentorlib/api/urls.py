from django.urls import path, include

urlpatterns = [
    path("users/", include("mentorlib.api.apps.users.urls")),
    path("configuration/", include("mentorlib.api.apps.configuration.urls")),
]
