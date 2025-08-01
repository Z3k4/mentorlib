from mentorlib.apps.courses.models import Course, CourseUploadFile
from mentorlib.apps.users.models import User, UserUpload, UploadMetadata
from mentorlib.settings import BASE_DIR
from pathlib import Path
import uuid
import filetype
from django.core.exceptions import PermissionDenied
import PyPDF2
from mentorlib.settings import UPLOADS_DIR


def get_file_extension(file):
    """
    Retrieve file extension base on MIME data
    """
    guess = filetype.guess(file)
    return guess.extension


def handle_course_files(course: Course, user: User, file):
    user_upload = handle_files(user, file)
    if user_upload:
        course_upload = CourseUploadFile(course=course, user_upload=user_upload)
        course_upload.save()


def save_file_metadata(user_upload: UserUpload, file):
    extension = get_file_extension(file)
    file_metadatas = {
        "name": file.name,
        "size": file.size,
        "extension": extension,
        "content_type": filetype.guess(file).mime,
    }

    if extension == "pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        file_metadatas["pages"] = len(pdf_reader.pages)

    for name, value in file_metadatas.items():
        metadata = UploadMetadata(user_upload=user_upload, name=name, value=value)
        metadata.save()


def handle_files(user: User, file) -> UserUpload:
    if not user.has_perm("userupload.upload_files"):
        raise PermissionDenied(f"{user} cannot upload files")

    random_uuid = str(uuid.uuid4())
    extension = get_file_extension(file)
    path = Path(f"users/{user.id}") / f"{random_uuid}.{extension}"

    absolute_path = Path(BASE_DIR) / UPLOADS_DIR
    file_path = absolute_path / path

    if not absolute_path.exists():
        absolute_path.mkdir(exist_ok=True, parents=True)

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    user_upload = UserUpload(
        file_path=path,
        user=user,
    )

    user_upload.save()

    save_file_metadata(user_upload, file)

    return user_upload
