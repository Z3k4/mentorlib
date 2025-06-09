from django.urls import path
from mentorlib.api.apps.configuration.views import DepartmentView, SemesterView, ResourceView, StudyYearView


urlpatterns = [
    path('resources', ResourceView.as_view(), name='resources'),
    path('departments', DepartmentView.as_view(), name='departments'),
    path('semesters', SemesterView.as_view(), name='semesters'),
    path('studyyears', StudyYearView.as_view(), name='studyyears'),
]