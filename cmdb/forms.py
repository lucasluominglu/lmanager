from django import forms
from cmdb.models import Idc


class IdcForm(forms.ModelForm):
    class Meta:
        model = Idc
        fields = ['name', 'remark']
        labels = {'name': '', 'remark': ''}
