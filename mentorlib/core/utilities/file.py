from mentorlib.apps.courses.models import Course
from mentorlib.apps.users.models import User


def handle_course_files(course: Course, files):
    print(course, files)


def handle_files(user: User, files):
    pass
