from django.db import models
from users.models import User


class AlumniProfile(models.Model):
    EDUCATION_CHOICES = (
        ('bachelor', '学士'),
        ('master', '硕士'),
        ('doctor', '博士'),
    )

    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )

    GRADUATION_STATUS_CHOICES = [
        (0, '未毕业'),
        (1, '已毕业'),
        (2, '审核中')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户', related_name='alumni_profile')
    student_id = models.CharField('学号', max_length=20, unique=True)
    ethnicity = models.CharField('民族', max_length=50, null=True, blank=True)
    gender = models.CharField('性别', max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField('出生日期', null=True, blank=True)
    education_level = models.CharField('学历', max_length=20, choices=EDUCATION_CHOICES)
    major = models.CharField('专业', max_length=100)
    class_name = models.CharField('班级', max_length=100)
    graduation_date = models.DateField('毕业日期', null=True, blank=True)
    current_company = models.CharField('当前公司', max_length=200, blank=True)
    position = models.CharField('职位', max_length=100, blank=True)
    work_city = models.CharField('工作城市', max_length=100, blank=True)
    address = models.CharField('联系地址', max_length=200, blank=True)
    mbti=models.CharField('MBTI',max_length=10,blank=True)
    internship = models.CharField('实习经历', max_length=200, blank=True)
    advantage = models.TextField('个人优势', blank=True)
    is_graduated = models.IntegerField(choices=GRADUATION_STATUS_CHOICES, default=0)
    application_status = models.IntegerField(
        default=0,
        help_text='申请状态：0-未申请，1-审批中，2-审批通过，3-审批不通过'
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"

    class Meta:
        db_table = 'alumni_profiles'
        verbose_name = '校友信息'
        verbose_name_plural = verbose_name


class AlumniApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', '审核中'),
        ('approved', '审核通过'),
        ('rejected', '审核不通过'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='申请人')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    apply_date = models.DateTimeField('申请时间', auto_now_add=True)
    review_date = models.DateTimeField('审核时间', null=True, blank=True)
    apply_reason = models.TextField('申请说明', blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_applications',
                                 verbose_name='审核人')

    class Meta:
        db_table = 'alumni_applications'
        verbose_name = '校友申请'
        verbose_name_plural = verbose_name
