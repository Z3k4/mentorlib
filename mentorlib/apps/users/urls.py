from django.urls import path

from mentorlib.apps.users import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("<id>/profile", views.profile_view, name="profile"),
    path("<id>/note/<resource_id>/", views.profile_note_view, name="note"),
]
