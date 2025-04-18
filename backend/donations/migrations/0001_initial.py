# Generated by Django 4.2.19 on 2025-03-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DonationProject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="捐赠项目")),
                ("type", models.CharField(max_length=50, verbose_name="捐赠类型")),
                ("purpose", models.TextField(verbose_name="捐赠目的")),
                (
                    "target_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=12, verbose_name="目标金额"
                    ),
                ),
                (
                    "current_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        verbose_name="当前金额",
                    ),
                ),
                (
                    "donor_count",
                    models.IntegerField(default=0, verbose_name="捐赠人数"),
                ),
                ("end_time", models.DateTimeField(verbose_name="截止时间")),
            ],
            options={
                "verbose_name": "捐赠项目",
                "verbose_name_plural": "捐赠项目",
            },
        ),
    ]
