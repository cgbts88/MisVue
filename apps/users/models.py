from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """
    用户信息
    """
    HK_CHOICES = ((True, '是'), (False, '否'))
    GENDER_CHOICES = (("male", "男"), ("female", "女"))

    en_name = models.CharField(max_length=20, default="", verbose_name="英文姓名")
    cn_name = models.CharField(max_length=20, blank=True, default="", verbose_name="中文姓名")
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, null=True, blank=True, verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    is_hk = models.BooleanField(choices=HK_CHOICES, default=False, verbose_name='是否港职')
    work_card = models.CharField(max_length=6, null=True, blank=True, verbose_name="工号")
    ext_num = models.CharField(max_length=4, verbose_name='座机')
    mobile = models.CharField(max_length=11, null=True, blank=True, default="", verbose_name="电话")
    email_password = models.CharField(max_length=16, null=True, blank=True, verbose_name="邮箱密码")
    department = models.ForeignKey("Department",  null=True, on_delete=models.SET_NULL, verbose_name="部门")
    location = models.ForeignKey('Location', null=True, on_delete=models.SET_NULL, verbose_name="位置")
    position = models.ForeignKey("Position", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="职位")
    permits = models.ManyToManyField("Permit", verbose_name="权限", blank=True)
    roles = models.ManyToManyField("system.Role", verbose_name="角色", blank=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        if self.is_hk:
            name = self.en_name
        elif not self.cn_name:
            name = self.en_name
        else:
            name = "{} ({})".format(self.en_name, self.cn_name)
        return name


class Department(models.Model):
    """
    部门信息
    """

    sort_number = models.FloatField(null=True, blank=True, verbose_name="编号")
    title = models.CharField(max_length=32, null=True, blank=True, verbose_name="名称")
    simple_title = models.CharField(max_length=32, unique=True, verbose_name="简写")
    leader = models.ForeignKey("UserProfile", blank=True, null=True, on_delete=models.SET_NULL,
                               related_name="leader", verbose_name="主管")
    clerk = models.ForeignKey("UserProfile", blank=True, null=True, on_delete=models.SET_NULL,
                              related_name="clerk", verbose_name="文员")
    asset_owner = models.ForeignKey("UserProfile", blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name="asset_owner", verbose_name="资产责任人")

    objects = models.Manager()

    class Meta:
        verbose_name = "部门信息"
        verbose_name_plural = verbose_name
        ordering = ['sort_number']

    def __repr__(self):
        return str('%s') % self.simple_title


class Position(models.Model):
    """
    职位信息
    """

    sort_number = models.FloatField(null=True, blank=True, verbose_name="编号")
    title = models.CharField(max_length=32, unique=True, verbose_name='名称')

    objects = models.Manager()

    class Meta:
        verbose_name = "职位信息"
        verbose_name_plural = verbose_name
        ordering = ['sort_number']

    def __str__(self):
        return self.title


class Location(models.Model):
    """
    位置信息
    """

    sort_number = models.FloatField(null=True, blank=True, verbose_name="编号")
    area = models.CharField(max_length=32, unique=True, verbose_name='区域')

    objects = models.Manager()

    class Meta:
        verbose_name = '位置信息'
        verbose_name_plural = verbose_name
        ordering = ['sort_number']

    def __str__(self):
        return self.area


class Permit(models.Model):
    """
    权限列表
    """

    sort_number = models.FloatField(null=True, blank=True, verbose_name="编号")
    title = models.CharField(max_length=32, unique=True, verbose_name='名称')
    mean = models.TextField(default="", blank=True, null=True, verbose_name="备注")

    objects = models.Manager()

    class Meta:
        verbose_name = '授权列表'
        verbose_name_plural = verbose_name
        ordering = ['sort_number']

    def __str__(self):
        return self.title


class PermitLog(models.Model):
    """
    授权记录
    """

    TYPES = (('update', '修改'), ('upload', '上传'))

    record_obj = models.ForeignKey("UserProfile", related_name='permit_proposer',
                                   on_delete=models.CASCADE, verbose_name='申请人')
    recorder = models.ForeignKey("UserProfile", related_name='permit_recorder', null=True,
                                 on_delete=models.SET_NULL, verbose_name='记录人')
    record_type = models.CharField(max_length=16, choices=TYPES, verbose_name='记录类型')
    record_time = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')
    remark = models.TextField(default="", verbose_name="备注")

    objects = models.Manager()

    class Meta:
        verbose_name = '授权记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.record_obj
