from django.core.exceptions import ValidationError

from rbac.forms.base import BaseModelForm
from rbac.models import UserInfo
from django import forms

class UserInfoModelForm(BaseModelForm):
    repassword = forms.CharField(required=True,label='确认密码')
    class Meta:
        model = UserInfo
        fields = ['name','password','repassword','email']

    # def clean(self):
    #     pwd =  self.cleaned_data.get('password')
    #     repwd = self.cleaned_data.get('repassword')
    #     if pwd != repwd:
    #         self.add_error('repassword',"两次密码输入不一致")

    def clean_repassword(self):
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')

        if pwd != repwd:
            raise ValidationError("两次密码输入不一致")
        return repwd

