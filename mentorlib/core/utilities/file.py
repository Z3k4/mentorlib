from mentorlib.apps.courses.models import Course, CourseUploadFile
from mentorlib.apps.users.models import UserUpload, User


def handle_course_files(course:Course, files):
    print(course, files)

def handle_files(user:User, files):
    user_upload =  UserUpload(user=user, )