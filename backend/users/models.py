from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', '校方管理员'),
        ('liaison', '校友联络人'),
        ('alumni', '未毕业校友'),
        ('graduated_alumni', '毕业校友')
    )
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )

    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField('手机号', max_length=20, blank=True)
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, default='male')
    department = models.CharField('学院', max_length=100, blank=True)
    graduation_year = models.IntegerField('毕业年份', null=True, blank=True)
    is_graduated = models.BooleanField('是否毕业', default=False)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    student_id = models.CharField('学号', max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
