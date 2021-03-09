from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from apps.utils.util import FileStorage


class Menu(models.Model):
    """
    菜单
    """
    sort_number = models.FloatField(verbose_name="编号")
    title = models.CharField(max_length=32, unique=True, verbose_name="菜单名")
    code = models.CharField(max_length=64, verbose_name="编码")
    url = models.CharField(max_length=128, unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['sort_number']

    @classmethod
    def get_menu_by_request_url(cls, url):
        try:
            return dict(menu=Menu.objects.get(url=url))
        except ObjectDoesNotExist:
            pass


class Role(models.Model):
    """
    角色：绑定权限
    """
    sort_number = models.FloatField(verbose_name="编号")
    title = models.CharField(max_length=32, unique=True, verbose_name="角色名称")
    permissions = models.ManyToManyField("Menu", blank=True, verbose_name="URL授权")

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name
        ordering = ['sort_number']


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

    def __str__(self):
        return self.email_host


class FileUpload(models.Model):
    file = models.FileField(upload_to='upload/', storage=FileStorage())

    objects = models.Manager()

    class Meta:
        verbose_name = '上传文件'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.file
