from django.db import models

class DonationProject(models.Model):
    name = models.CharField(max_length=200, verbose_name='捐赠项目')
    type = models.CharField(max_length=50, verbose_name='捐赠类型')
    purpose = models.TextField(verbose_name='捐赠目的')
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='目标金额')
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='当前金额')
    donor_count = models.IntegerField(default=0, verbose_name='捐赠人数')
    end_time = models.DateTimeField(verbose_name='截止时间')

    class Meta:
        verbose_name = '捐赠项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name 