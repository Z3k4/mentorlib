from django.db.models.signals import pre_delete
from django.dispatch import receiver
from mentorlib.apps.users.models import UserUpload


@receiver(pre_delete, sender=UserUpload)
def delete_file(sender: UserUpload, instance, **kwargs):
    pass
