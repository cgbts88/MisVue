from django.db import models
from django.contrib.auth import get_user_model

from apps.users.models import Department

User = get_user_model()


class TypeCode(models.Model):
    """
    分类编码
    """

    simple_code = models.CharField(max_length=32, unique=True, verbose_name="简写分类")
    en_code = models.CharField(max_length=32, verbose_name="英文分类")
    cn_code = models.CharField(max_length=32, verbose_name="中文分类")

    objects = models.Manager()

    class Meta:
        verbose_name = "分类编码"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.simple_code


class Attribute(models.Model):
    """
    属性信息
    """
    NETWORK_CHOICES = ((True, '是'), (False, '否'))

    type = models.ForeignKey("TypeCode", null=True, on_delete=models.CASCADE, verbose_name="分类")
    brand = models.CharField(max_length=32, verbose_name="品牌")
    model = models.CharField(max_length=32, verbose_name="型号")
    parameter = models.CharField(max_length=128, null=True, blank=True, verbose_name="参数")
    is_network = models.BooleanField(choices=NETWORK_CHOICES, default=True, verbose_name='是否网络设备')

    objects = models.Manager()

    class Meta:
        verbose_name = "属性信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return str('%s %s') % (self.brand, self.model)


class Stock(models.Model):
    """
    库存信息
    """

    STATUS = (('free', '闲置'), ('used', '在用'), ('disuse', '弃用'), ('scrap', '报废'))

    it_num = models.CharField(max_length=32, verbose_name="EDP编号")
    acc_num = models.CharField(max_length=32, blank=True, null=True, verbose_name="ACC编号")
    sn = models.CharField(max_length=32, verbose_name="序列号")
    mac = models.CharField(max_length=32, null=True, blank=True, verbose_name="MAC地址")
    rmb = models.IntegerField(blank=True, null=True, verbose_name="人民币")
    hkd = models.IntegerField(blank=True, null=True, verbose_name="港币")
    buy_date = models.DateField(blank=True, null=True, verbose_name="购买日期")
    warranty_date = models.DateField(blank=True, null=True, verbose_name="到保日期")
    state = models.CharField(choices=STATUS, max_length=8, default="free", verbose_name="资产状态")
    model = models.ForeignKey("Attribute", null=True, on_delete=models.SET_NULL, verbose_name="型号")
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL,
                                   related_name="stock_department", verbose_name="库存部门")

    objects = models.Manager()

    class Meta:
        verbose_name = "库存信息"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.it_num


class NetworkDevice(models.Model):
    """
    网络设备
    """

    device_name = models.CharField(unique=True, max_length=32, verbose_name="设备名")
    ip = models.GenericIPAddressField(unique=True, blank=True, null=True,  verbose_name="IP地址")
    login_name = models.CharField(max_length=32, blank=True, null=True, verbose_name="登录名")
    login_pwd = models.CharField(max_length=32, blank=True, null=True, verbose_name="登录密码")
    remark = models.TextField(default="", blank=True, null=True, verbose_name="备注信息")
    asset_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="network_asset_user", verbose_name="使用人")
    stock = models.ForeignKey("Stock", null=True, blank=True, on_delete=models.SET_NULL,
                              verbose_name="设备编号")

    objects = models.Manager()

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.device_name


class OtherDevice(models.Model):
    """
    其它设备
    """

    remark = models.TextField(default="", blank=True, null=True, verbose_name="备注信息")
    asset_user = models.ForeignKey(User, blank=True, null=True,
                                   on_delete=models.SET_NULL, related_name="other_asset_user",
                                   verbose_name="使用人")
    stock = models.ForeignKey("Stock", null=True, blank=True, on_delete=models.SET_NULL,
                              verbose_name="设备编号")

    objects = models.Manager()

    class Meta:
        verbose_name = "其它设备"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.stock


class RecordLog(models.Model):
    """
    记录日志
    """
    TYPES = (('create', '创建'), ('update', '修改'), ('transfer', '转移'), ('scrap', '报废'))

    record_obj = models.ForeignKey("Stock", on_delete=models.CASCADE, verbose_name="记录对象")
    recorder = models.ForeignKey(User, related_name='asset_recorder', null=True, on_delete=models.SET_NULL,
                                 verbose_name="记录人")
    record_time = models.DateTimeField(auto_now_add=True, verbose_name="记录时间")
    record_type = models.CharField(choices=TYPES, max_length=16, default="create", verbose_name="记录类型")
    remark = models.TextField(default="", verbose_name="内容")

    objects = models.Manager()

    class Meta:
        verbose_name = "记录日志"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.record_obj


class AssetOrder(models.Model):
    """
    资产管理
    """
    num = models.CharField(max_length=32, null=True, blank=True, verbose_name="单号")
    edp_asset = models.CharField(max_length=64, null=True, blank=True, verbose_name="电脑部资产")
    target_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING,
                                          verbose_name="目标部门")
    target_asset = models.CharField(max_length=64, null=True, blank=True, verbose_name="目标部门资产")
    transfer_time = models.DateTimeField(auto_now_add=True, verbose_name="转移时间")
    remark = models.TextField(default="", null=True, blank=True, verbose_name="备注")

    objects = models.Manager()

    class Meta:
        verbose_name = "资产管理"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.num
