from django.db import models
from django.core.exceptions import ValidationError
from users.models import User


class Association(models.Model):
    TYPE_CHOICES = (
        ('general', '总会'),
        ('college', '学院校友会'),
        ('local', '地方校友会'),
        ('overseas', '海外校友会'),
        ('industry', '行业校友会'),
    )

    name = models.CharField('名称', max_length=100, unique=True)
    type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES)
    description = models.TextField('简介', blank=True)
    founding_date = models.DateField('成立日期')
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_associations',
                             verbose_name='会长')
    members = models.ManyToManyField(User, through='AssociationMember', related_name='joined_associations',
                                   verbose_name='成员')
    image = models.ImageField('图片', upload_to='association_images/', null=True, blank=True)
    
    class Meta:
        db_table = 'associations'
        verbose_name = '校友会'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=['type'],
                condition=models.Q(type='general'),
                name='unique_general_association'
            )
        ]

    def clean(self):
        if self.type == 'general':
            if not self.leader.is_superuser:
                raise ValidationError('总会会长必须是管理员')
        else:
            if not hasattr(self.leader, 'role') or self.leader.role != 'liaison':
                raise ValidationError('分会会长必须是校友联络员')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class AssociationMember(models.Model):
    ROLE_CHOICES = (
        ('president', '会长'),
        ('member', '会员'),
    )
    
    STATUS_CHOICES = (
        (0, '默认'),
        (1, '申请中'),
        (2, '已通过'),
        (3, '已拒绝'),
    )

    association = models.ForeignKey(Association, on_delete=models.CASCADE, verbose_name='校友会')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES, default='member')
    join_date = models.DateField('加入日期', auto_now_add=True)
    status = models.IntegerField('状态', choices=STATUS_CHOICES, default=0)

    class Meta:
        db_table = 'association_members'
        verbose_name = '校友会成员'
        verbose_name_plural = verbose_name
        unique_together = ['association', 'user']  # 一个用户在同一个校友会中只能有一个身份

    def clean(self):
        if not self.user.is_graduated and self.status != 1:  # 申请中状态不检查毕业状态
            raise ValidationError('只有已毕业的校友才能加入校友会')
        
        if self.role == 'president':
            if self.association.type == 'general' and not self.user.is_superuser:
                raise ValidationError('总会会长必须是管理员')
            elif self.association.type != 'general' and not hasattr(self.user, 'role') or self.user.role != 'liaison':
                raise ValidationError('分会会长必须是校友联络员')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
