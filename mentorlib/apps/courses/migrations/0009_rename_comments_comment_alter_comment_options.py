# Generated by Django 5.2.3 on 2025-06-23 18:03

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0008_alter_askedcourse_approved_date"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Comments",
            new_name="Comment",
        ),
        migrations.AlterModelOptions(
            name="comment",
            options={
                "permissions": [("change_status", "Allow user to lock / cancel course")]
            },
        ),
    ]
