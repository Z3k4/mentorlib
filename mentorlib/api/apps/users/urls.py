from django.urls import path
from mentorlib.api.apps.users.views import UsersView


urlpatterns = [
    path('', UsersView.as_view(), name='users'),
]