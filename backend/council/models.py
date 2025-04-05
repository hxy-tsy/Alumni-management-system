from django.db import models
from users.models import User

class CouncilMeeting(models.Model):
    name = models.CharField(max_length=200, verbose_name='理事会名称')
    content = models.TextField(verbose_name='内容')
    location = models.CharField(max_length=200, verbose_name='地点')
    invitees = models.ManyToManyField(User, related_name='invited_meetings', verbose_name='邀请人员')
    meeting_time = models.DateTimeField(verbose_name='召开时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetings', verbose_name='召开人')
    invitation_sent = models.BooleanField(default=False, verbose_name='是否已发送邀请')

    class Meta:
        verbose_name = '理事会'
        verbose_name_plural = verbose_name
        ordering = ['-meeting_time']

    def __str__(self):
        return self.name 