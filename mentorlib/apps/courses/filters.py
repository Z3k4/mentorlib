from django_filters import rest_framework as filters
from mentorlib.apps.courses.models import Course
from mentorlib.apps.configuration.models import Resource

class CourseFilter(filters.FilterSet):
    resource = filters.ModelMultipleChoiceFilter(field_name="resource__id",
                                                 to_field_name="id",
                                                 queryset=Resource.objects.all())

    class Meta:
        model = Course
        fields = ['resource', 'mentor']
 