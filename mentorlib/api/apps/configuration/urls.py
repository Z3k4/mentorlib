from django.urls import path
from mentorlib.api.apps.configuration.views import (
    DepartmentView,
    SemesterView,
    ResourceView,
    StudyYearView,
    AllDepartmentsView,
    AllResourcesView,
    AllSemestersView,
    AllStudyYearsView,
)


urlpatterns = [
    path("resources", AllResourcesView.as_view(), name="resources"),
    path("resources/<resource_id>/", ResourceView.as_view(), name="resources"),
    path("departments", AllDepartmentsView.as_view(), name="departments"),
    path("departments/<department_id>/", DepartmentView.as_view(), name="departments"),
    path("semesters", AllSemestersView.as_view(), name="semesters"),
    path("semesters/<semester_id>/", SemesterView.as_view(), name="semesters"),
    path("studyyears", AllStudyYearsView.as_view(), name="studyyears"),
    path("studyyears/<studyyear_id>/", StudyYearView.as_view(), name="studyyears"),
]
