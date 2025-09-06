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
    """Handle and attach uploaded file to a course"""
    user_upload = handle_files(user, file)
    if user_upload:
        course_upload = CourseUploadFile(course=course, user_upload=user_upload)
        course_upload.save()


def save_file_metadata(user_upload: UserUpload, file) -> None:
    """
    Save all interesting metadata from file, like size, extension, content_type
    """
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
    """
    Save uploaded file into user directory
    """
    if not user.has_perm("userupload.upload_files"):
        raise PermissionDenied(f"{user} cannot upload files")

    file_name = f"{uuid.uuid4()}.{get_file_extension(file)}"
    user_dir = Path(f"users/{user.id}")

    absolute_path = Path(BASE_DIR) / UPLOADS_DIR
    file_path = absolute_path / user_dir / file_name

    if not (absolute_path / user_dir).exists():
        (absolute_path / user_dir).mkdir(exist_ok=True, parents=True)

    with open(file_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    user_upload = UserUpload(
        file_path=user_dir / file_name,
        user=user,
    )

    user_upload.save()

    save_file_metadata(user_upload, file)

    return user_upload
