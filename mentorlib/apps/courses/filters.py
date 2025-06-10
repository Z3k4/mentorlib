from django_filters import rest_framework as filters
from mentorlib.apps.courses.models import Course
from mentorlib.apps.configuration.models import Resource
from django.db.models import Q

class CourseFilter(filters.FilterSet):
    resource = filters.ModelMultipleChoiceFilter(field_name="resource__id",
                                                 to_field_name="id",
                                                 queryset=Resource.objects.all())
    
    mentor = filters.CharFilter(method='search_mentor')

    def search_mentor(self, queryset, name, value):
        
        return queryset.filter(Q(mentor__first_name__icontains=value) | Q(mentor__last_name__icontains=value)) 

    class Meta:
        model = Course
        fields = ['resource', 'mentor']
