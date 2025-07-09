from mentorlib.apps.configuration.templatetags.configuration_utils import (
    format_date_to_local,
)


def serialize_chat(user, message):
    user_json = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "id": user.id,
    }

    return {"user": user_json, "message": message, "date": format_date_to_local()}
