from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from apps.utils.util import FileStorage


class Menu(models.Model):
    """
    菜单
    """
    sort = models.FloatField(verbose_name="排序标记")
    name = models.CharField(max_length=32, unique=True, verbose_name="菜单名")
    icon = models.CharField(max_length=64, null=True, blank=True, verbose_name="图标")
    path = models.CharField(max_length=128, null=True, blank=True, verbose_name="链接地址")
    is_frame = models.BooleanField(default=False, verbose_name="外部菜单")
    is_show = models.BooleanField(default=True, verbose_name="显示标记")
    component = models.CharField(max_length=256, null=True, blank=True, verbose_name="组件")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")

    objects = models.Manager()

    def __repr__(self):
        return str('%s') % self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['sort']


class Permission(models.Model):
    """
    权限
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="权限名")
    method = models.CharField(max_length=64, null=True, blank=True, verbose_name="方法")
    pid = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父权限")

    def __repr__(self):
        return str('%s') % self.name

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Role(models.Model):
    """
    角色：绑定权限
    """
    sort = models.FloatField(verbose_name="排序标记")
    name = models.CharField(max_length=32, unique=True, verbose_name="角色")
    permissions = models.ManyToManyField("Permission", blank=True, verbose_name="权限")
    menus = models.ManyToManyField("Menu", blank=True, verbose_name="菜单")
    desc = models.CharField(max_length=64, blank=True, null=True, verbose_name="描述")

    objects = models.Manager()

    def __repr__(self):
        return str('%s') % self.name

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        ordering = ['sort']


class EmailSetup(models.Model):
    email_host = models.CharField(max_length=32, verbose_name='SMTP服务器')
    email_port = models.IntegerField(verbose_name='SMTP端口')
    email_user = models.EmailField(max_length=128, verbose_name='邮箱帐号')
    email_password = models.CharField(max_length=32, verbose_name='邮箱密码')

    objects = models.Manager()

    class Meta:
        verbose_name = '发件邮箱设置'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __repr__(self):
        return str('%s') % self.email_host


class FileUpload(models.Model):
    file = models.FileField(upload_to='upload/', storage=FileStorage())

    objects = models.Manager()

    class Meta:
        verbose_name = '上传文件'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __repr__(self):
        return str('%s') % self.file
