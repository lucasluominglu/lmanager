from django import forms
from cmdb.models import *


class IdcForm(forms.ModelForm):
    class Meta:
        model = Idc
        fields = ['name', 'remark']
        labels = {'name': '机房', 'remark': '备注'}


class HostForm(forms.ModelForm):
	class Meta:
		model = Host
		fields = ['idc','hostname','num','application']
		labels = {'idc': '机房', 'hostname': '主机名','num': '编号', 'application': '应用'}


class HostInfoForm(forms.ModelForm):
	class Meta:
		model = HostInfo
		fields = ['manufacturer','productmode','serialnumber','cpu','mem','os','disk']
		labels = {'manufacturer':'厂商','productmode':'产品型号',
		 'serialnumber':'产品序列号', 'cpu':'CPU核数', 'mem':'内存', 'os':'操作系统', 'disk':'硬盘大小' }


class IpForm(forms.ModelForm):
	class Meta:
		model = Ip
		fields = ['ip1','ip2']
		labels = {'ip1':'ip1','ip2':'ip2'}