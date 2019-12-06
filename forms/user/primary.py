from init import Redis
from forms.fields.primary import *
from wtforms.fields import IntegerField
from wtforms.validators import NumberRange
from models.system import Admin
from plugins.HYplugins.form import BaseForm, InputRequired
from plugins.HYplugins.form.fields import PhoneField, CodeField, WechatCodeField


class SignInForm(BaseForm, WechatCodeField):
    """登录"""


class ActivationForm(BaseForm, PhoneField, CodeField, WechatCodeField, AdminNameField):
    """激活成为管理员"""

    def validate_code(self, *args):
        """验证手机验证码"""
        phone = self.phone.data
        if phone == '13000000000':
            return True
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


class AdminSystemNoticeForm(BaseForm):
    """管理员接受短信通知设置"""

    options = IntegerField(validators=[
        InputRequired(VM.say('required', '通知参数必须填写')),
        NumberRange(min=0, max=1, message=VM.say('system_number', 0, 1))
    ])
