from django.core.exceptions import ValidationError

from rbac.forms.base import BaseModelForm
from rbac.models import UserInfo
from django import forms

class UserInfoModelForm(BaseModelForm):
    repassword = forms.CharField(required=True,label='确认密码',widget=forms.PasswordInput())
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


class UserInfoUpdateModelForm(BaseModelForm):
    class Meta:
        model = UserInfo
        fields = ['name','email']

    # def clean(self):
    #     pwd =  self.cleaned_data.get('password')
    #     repwd = self.cleaned_data.get('repassword')
    #     if pwd != repwd:
    #         self.add_error('repassword',"两次密码输入不一致")

class UserInfoResetPwdModelForm(BaseModelForm):
    oripassword = forms.CharField(required=True,label='原密码',widget=forms.PasswordInput())
    repassword = forms.CharField(required=True,label='确认密码',widget=forms.PasswordInput())

    class Meta:
        model = UserInfo
        fields = ['oripassword','password','repassword']


    def clean_oripassword(self):
        oripassword = self.cleaned_data.get('oripassword')
        if self.instance.password != oripassword:
            self.add_error('oripassword',"原密码不正确")


    def clean_repassword(self):
        pwd = self.cleaned_data.get('password')
        repwd = self.cleaned_data.get('repassword')

        if pwd != repwd:
            raise ValidationError("两次密码输入不一致")
        return repwd


