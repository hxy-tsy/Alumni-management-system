# Generated by Django 4.2.19 on 2025-03-02 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alumni", "0002_alumniprofile_avatar_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="alumniprofile",
            name="application_status",
            field=models.IntegerField(
                default=0,
                help_text="申请状态：0-未申请，1-审批中，2-审批通过，3-审批不通过",
            ),
        ),
    ]
