# Generated by Django 4.2.19 on 2025-02-28 16:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AlumniProfile",
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
                (
                    "student_id",
                    models.CharField(max_length=20, unique=True, verbose_name="学号"),
                ),
                (
                    "ethnicity",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="民族"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("male", "男"), ("female", "女")],
                        max_length=10,
                        null=True,
                        verbose_name="性别",
                    ),
                ),
                (
                    "birth_date",
                    models.DateField(blank=True, null=True, verbose_name="出生日期"),
                ),
                (
                    "education_level",
                    models.CharField(
                        choices=[
                            ("bachelor", "学士"),
                            ("master", "硕士"),
                            ("doctor", "博士"),
                        ],
                        max_length=20,
                        verbose_name="学历",
                    ),
                ),
                ("major", models.CharField(max_length=100, verbose_name="专业")),
                ("class_name", models.CharField(max_length=100, verbose_name="班级")),
                (
                    "graduation_date",
                    models.DateField(blank=True, null=True, verbose_name="毕业日期"),
                ),
                (
                    "current_company",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="当前公司"
                    ),
                ),
                (
                    "position",
                    models.CharField(blank=True, max_length=100, verbose_name="职位"),
                ),
                (
                    "work_city",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="工作城市"
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="联系地址"
                    ),
                ),
                (
                    "is_graduated",
                    models.BooleanField(default=False, verbose_name="是否毕业"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="用户",
                    ),
                ),
            ],
            options={
                "verbose_name": "校友信息",
                "verbose_name_plural": "校友信息",
                "db_table": "alumni_profiles",
            },
        ),
        migrations.CreateModel(
            name="AlumniApplication",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "审核中"),
                            ("approved", "审核通过"),
                            ("rejected", "审核不通过"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="状态",
                    ),
                ),
                (
                    "apply_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="申请时间"),
                ),
                (
                    "review_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="审核时间"
                    ),
                ),
                ("apply_reason", models.TextField(blank=True, verbose_name="申请说明")),
                (
                    "reviewer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviewed_applications",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="审核人",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="申请人",
                    ),
                ),
            ],
            options={
                "verbose_name": "校友申请",
                "verbose_name_plural": "校友申请",
                "db_table": "alumni_applications",
            },
        ),
    ]
