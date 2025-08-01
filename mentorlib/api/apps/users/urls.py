from django.urls import path
from mentorlib.api.apps.users.views import (
    AllUsersView,
    UserView,
    UserNotesView,
    NotificationView,
)


urlpatterns = [
    path("", AllUsersView.as_view(), name="users"),
    path("<int:user_id>/", UserView.as_view(), name="user"),
    path("<int:user_id>/notes/", UserNotesView.as_view(), name="user_notes"),
    path("notifications/", NotificationView.as_view(), name="user_notifications"),
]
