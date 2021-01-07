from rbac.forms.base import BaseModelForm
from rbac.models import Role

class RoleModelForm(BaseModelForm):

    class Meta:
        model = Role
        fields = ['title']
        # fields = '__all__'

