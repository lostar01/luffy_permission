from django.forms import ModelForm
from django import forms
class BaseModelForm(ModelForm):
    exclude_bootstrap = []
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #自定义功能
        for k,field in self.fields.items():
            if k in self.exclude_bootstrap:
                continue
            if k == 'password' or k == 'repassword':
                field.widget = forms.PasswordInput()
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
