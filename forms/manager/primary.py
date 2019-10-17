from forms.fields.primary import *
from plugins.HYplugins.form import BaseForm, ListPage, IntegerField, NumberRange
from plugins.HYplugins.form.fields import PhoneField


class UserListForm(BaseForm, UserGenreField, ListPage):
    """用户列表"""

    phone = wtforms.StringField(validators=[
        Optional(),
        Length(max=11, message=VM.say('length', '手机号', 1, 11))
    ])

    name = wtforms.StringField(validators=[
        Optional(),
        Length(max=10, message=VM.say('length', '名称', 1, 10))
    ])


class FactoryOrderListForm(BaseForm, ListPage):
    """厂家订单列表"""

    create_time_sort = IntegerField(validators=[
        Optional(),
        NumberRange(min=0, max=1, message=VM.say('system_number', 0, 1))
    ])


class OrderEntrustForm(BaseForm):
    """订单指派/委托给驾驶员"""