import json
from channels.generic.websocket import AsyncWebsocketConsumer
from mentorlib.apps.configuration.templatetags.configuration_utils import (
    format_date_to_local,
)
from mentorlib.apps.courses.models import Comment, Course
from channels.db import database_sync_to_async
from mentorlib.apps.users.utils import notify_users_related_to_course
from mentorlib.apps.users.models import NotificationType


@database_sync_to_async
def create_comment(course_id, message, user):
    course = Course.objects.get(id=course_id)
    comment = Comment(course=course, comment=message, user=user)
    comment.save()

    notification_type = NotificationType.objects.get(short_name="course_comment")
    variables = {"comment": message}
    notify_users_related_to_course(course, notification_type, variables)

    return comment


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]
        course_id = text_data_json["course"]

        if user:
            comment = await create_comment(course_id, message, user)
            user_json = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "id": user.id,
            }
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": {
                        "user": user_json,
                        "message": {
                            "text": message,
                            "date": format_date_to_local(comment.date),
                        },
                    },
                },
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
