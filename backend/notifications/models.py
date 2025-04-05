from django.db import models
from users.models import User


class Notification(models.Model):
    TYPE_CHOICES = (
        ('news', '新闻通知'),
        ('activity', '活动通知'),
        ('greeting', '节日祝福'),
    )

    STATUS_CHOICES = (
        (0, '发送成功'),
        (1, '发送失败'),
    )

    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', verbose_name='发送人')
    receivers = models.ManyToManyField(User, related_name='received_notifications', verbose_name='接收人')
    send_time = models.DateTimeField('发送时间', null=True, blank=True)
    status = models.IntegerField('发送状态', choices=STATUS_CHOICES, default=0)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = '通知'
        verbose_name_plural = verbose_name
