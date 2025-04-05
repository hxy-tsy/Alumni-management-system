from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Activity(models.Model):
    STATUS_CHOICES = (
        (0, '默认'),
        (1, '申请中'),
        (2, '已通过'),
        (3, '已拒绝'),
    )

    name = models.CharField('活动名称', max_length=100, null=True, blank=True)
    description = models.TextField('活动介绍', null=True, blank=True)
    applicant_name = models.CharField('申请人姓名', max_length=50, null=True, blank=True)
    phone = models.CharField('联系电话', max_length=20, null=True, blank=True)
    organization = models.CharField('举办组织', max_length=100, null=True, blank=True)
    venue = models.CharField('场地设施', max_length=200, null=True, blank=True)
    apply_time = models.DateTimeField('申请时间', auto_now_add=True, null=True, blank=True)
    event_time = models.DateTimeField('活动举办时间', null=True, blank=True)
    # members = models.ManyToManyField(User, through='ActivityMember', related_name='joined_activities',
    #                                  verbose_name='成员')
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=0)

    class Meta:
        db_table = 'activities'
        verbose_name = '校友活动'
        verbose_name_plural = verbose_name
        ordering = ['-apply_time']

    def __str__(self):
        return self.name


class ActivityMember(models.Model):
    STATUS_CHOICES = (
        (0, '默认'),
        (1, '申请中'),
        (2, '已通过'),
        (3, '已拒绝'),
    )
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='members', verbose_name='活动')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_memberships', verbose_name='用户')
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=1)


    class Meta:
        db_table = 'activity_members'
        verbose_name = '活动成员'
        verbose_name_plural = verbose_name
        unique_together = ('activity', 'user')  # 确保每个用户只能报名一次同一个活动

    def clean(self):
        if not self.user.is_graduated and self.status != 1:  # 申请中状态不检查毕业状态
            raise ValidationError('只有已毕业的校友才能报名参加活动')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.activity.name}"


class ActivityFeedback(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='feedbacks')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activity', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s feedback for {self.activity.name}"
