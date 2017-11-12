from django.db import models
from django.contrib.auth.models import User


class Idc(models.Model):
    """定义机房类"""
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=40, verbose_name='机房名称')
    remark = models.CharField(max_length=50, verbose_name='备注')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = '机房'

    def __str__(self):
        return self.name


class Ip(models.Model):
    host = models.ForeignKey("Host")
    ip = models.GenericIPAddressField(verbose_name="ip")

    def __str__(self):
        return self.ip


class Host(models.Model):
    """定义主机列表"""
    idc = models.ForeignKey(Idc)
    date_added = models.DateTimeField(auto_now=True)
    hostname = models.CharField(max_length=40, verbose_name='主机名称')
    num = models.CharField(max_length=20, verbose_name='编号')
    application = models.CharField(max_length=40, verbose_name='应用')

    class Meta:
        verbose_name = '主机列表'
        verbose_name_plural = '主机列表'

    def __str__(self):
        return self.hostname


class HostInfo(models.Model):
    '''定义主机详细信息'''
    host = models.ForeignKey(Host)
    manufacturer = models.CharField(max_length=40, verbose_name='厂商')
    productmode = models.CharField(max_length=40, verbose_name='产品型号')
    serialnumber = models.CharField(max_length=40, verbose_name='产品序列号')
    cpu = models.CharField(max_length=40, null=True,
                           blank=True, verbose_name='CPU核数')
    mem = models.CharField(max_length=40, verbose_name='内存')
    os = models.CharField(max_length=40, verbose_name='操作系统')
    disk = models.CharField(max_length=40, verbose_name='硬盘大小')

    class Meta:
        verbose_name = '主机信息'
        verbose_name_plural = '主机信息'

    def __str__(self):
        return self.host.hostname
