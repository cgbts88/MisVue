from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class WorkOrder(models.Model):
    """
    日常工单
    """

    STATUS = (('wait', '等待处理'), ('process', '正在处理'), ('finish', '处理完毕'), ('confirm', '确认完成'))
    TYPES = (('normal', '普通问题'), ('email', '邮件问题'), ('erp', 'ERP问题'),
             ('print', '打印问题'), ('transmission', '上传下载'))

    num = models.CharField(max_length=32, unique=True, verbose_name='单号')
    type = models.CharField(max_length=16, choices=TYPES, default='normal', verbose_name='类型')
    content = models.TextField(max_length=512, verbose_name='内容')
    state = models.CharField(max_length=16, blank=True, choices=STATUS, default='wait', verbose_name='状态')
    proposer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发起人')

    class Meta:
        verbose_name = '日常工单'
        verbose_name_plural = verbose_name

    objects = models.Manager()

    def __str__(self):
        return self.num

    def format_content(self):
        if len(str(self.content)) > 16:
            return '{}...'.format(str(self.content)[0:16])
        else:
            return str(self.content)

    format_content.allow_tags = True


class WorkOrderLog(models.Model):
    """
    Form A  日常工单记录
    """

    TYPES = (('create', '创建'), ('update', '修改'), ('process', '处理'), ('finish', '完成'), ('confirm', '确认'))

    record_obj = models.ForeignKey("WorkOrder", verbose_name='单号', on_delete=models.CASCADE)
    recorder = models.ForeignKey(User, verbose_name='记录人', on_delete=models.CASCADE)
    record_type = models.CharField(max_length=16, choices=TYPES, verbose_name='记录类型')
    record_time = models.DateTimeField(auto_now_add=True, verbose_name='记录时间')
    remark = models.TextField(default="", verbose_name="备注")

    objects = models.Manager()

    class Meta:
        verbose_name = '日常工单记录'
        verbose_name_plural = verbose_name
