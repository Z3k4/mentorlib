from rest_framework import serializers
from mentorlib.apps.configuration.models import Department, Semester, Resource, StudyYear

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StudyYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyYear
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    year = StudyYearSerializer()
    class Meta:
        model = Semester
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    department = DepartmentSerializer()
    class Meta:
        model = Resource
        fields = '__all__'
