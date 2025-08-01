from rest_framework.views import APIView
from rest_framework.response import Response
from mentorlib.api.apps.configuration.serializers import (
    DepartmentSerializer,
    StudyYearSerializer,
    ResourceSerializer,
    SemesterSerializer,
)
from mentorlib.apps.configuration.models import (
    Department,
    Semester,
    Resource,
    StudyYear,
)


class DepartmentView(APIView):
    def get(self, request, department_id):
        item = Department.objects.get(id=department_id)
        serializer = DepartmentSerializer(item)
        return Response(serializer.data)


class StudyYearView(APIView):
    def get(self, request, studyyear_id):
        item = StudyYear.objects.get(id=studyyear_id)
        serializer = StudyYearSerializer(item)
        return Response(serializer.data)


class SemesterView(APIView):
    def get(self, request, semester_id):
        item = Semester.objects.get(id=semester_id)
        serializer = SemesterSerializer(item)
        return Response(serializer.data)


class ResourceView(APIView):
    def get(self, request, resource_id):
        item = Resource.objects.get(id=resource_id)
        serializer = ResourceSerializer(item)
        return Response(serializer.data)


class AllDepartmentsView(APIView):
    def get(self, request):
        items = Department.objects.all()
        serializer = DepartmentSerializer(items, many=True)
        return Response(serializer.data)


class AllStudyYearsView(APIView):
    def get(self, request):
        items = StudyYear.objects.all()
        serializer = StudyYearSerializer(items, many=True)
        return Response(serializer.data)


class AllSemestersView(APIView):
    def get(self, request):
        items = Semester.objects.all()
        serializer = SemesterSerializer(items, many=True)
        return Response(serializer.data)


class AllResourcesView(APIView):
    def get(self, request):
        items = Resource.objects.all()
        serializer = ResourceSerializer(items, many=True)
        return Response(serializer.data)
