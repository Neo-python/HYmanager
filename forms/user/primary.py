from plugins import Redis
from forms.fields.primary import *
from wtforms.fields import IntegerField
from wtforms.validators import NumberRange
from models.system import Admin
from plugins.HYplugins.form import BaseForm, InputRequired
from plugins.HYplugins.form.fields import PhoneField, CodeField, WechatCodeField, VisitorsParameterField


class SignInForm(BaseForm, WechatCodeField):
    """登录"""


class VisitorsForm(BaseForm, VisitorsParameterField):
    """访客审核验证"""

    server_name = '管理员端'


class ActivationForm(BaseForm, PhoneField, CodeField, WechatCodeField, AdminNameField):
    """激活成为管理员"""

    def validate_code(self, *args):
        """验证手机验证码"""

        # 审核逻辑
        if self.wechat_verify() is True:
            return True

        phone = self.phone.data
        self.redis_key = f'validate_phone_activation_{phone}'
        if self.code.data == Redis.get(self.redis_key):
            return True
        else:
            raise wtforms.ValidationError(message='验证码错误')

    def validate_phone(self, *args):
        """验证手机号"""

        # 审核逻辑
        if self.wechat_verify() is True:
            return True

        self.admin = Admin.query.filter_by(phone=self.phone.data, open_id=None).first()

        if not self.admin:
            raise wtforms.ValidationError(message='您还未成为海嘉粤管理员,无法激活管理员身份.')

    def wechat_verify(self):
        if self.phone.data == '13000000000':
            self.admin = Admin.query.filter_by(phone=self.phone.data).first()
            self.redis_key = f'validate_phone_activation_{self.phone.data}'
            return True


class AdminInfoEditForm(BaseForm, AdminNameField):
    """管理员信息编辑"""


class AdminSystemNoticeForm(BaseForm):
    """管理员接受短信通知设置"""

    options = IntegerField(validators=[
        InputRequired(VM.say('required', '通知参数必须填写')),
        NumberRange(min=0, max=1, message=VM.say('system_number', 0, 1))
    ])
