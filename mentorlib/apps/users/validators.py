import filetype
from django.forms import ValidationError

class FileValidator():
    allowed_extensions:list[str]
    def __init__(self, allowed_extensions):
        self.allowed_extensions = allowed_extensions

    def __call__(self, value):
        breakpoint()
        guess = filetype.guess(value)
        if not guess:
            raise ValidationError(
                ("%(value)s is not a valid file"),
                params={"value": value},
            )

        if guess.extension not in self.allowed_extensions:
            raise ValidationError(
                ("%(value)s file extension is not allowed"),
                params={"value": value},
            )
    