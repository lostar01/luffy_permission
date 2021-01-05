from django.forms import ModelForm
from rbac.models import UserInfo
from django import forms

class UserInfoModelForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(UserInfoModelForm, self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            if name == 'password':
                field.widget=forms.PasswordInput()
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label