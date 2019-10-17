import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from init import Redis
from forms.fields.primary import *
from models.HYModels.system import Admin
from plugins.HYplugins.form import BaseForm
from plugins.HYplugins.form.fields import PhoneField, CodeField, OpenIdField


class ActivationForm(BaseForm, PhoneField, CodeField, OpenIdField, AdminNameField):
    """激活成为管理员"""

    def validate_code(self, *args):
        """验证手机验证码"""
        phone = self.phone.data
        self.redis_key = f'validate_phone_activation_{phone}'
        if self.code.data == Redis.get(self.redis_key):
            return True
        else:
            raise wtforms.ValidationError(message='验证码错误')

    def validate_phone(self, *args):
        """验证手机号"""
        self.admin = Admin.query.filter_by(phone=self.phone.data, open_id=None).first()

        if not self.admin:
            raise wtforms.ValidationError(message='您还未成为海嘉粤管理员,无法激活管理员身份.')


class AdminInfoEditForm(BaseForm, AdminNameField):
    """管理员信息编辑"""
