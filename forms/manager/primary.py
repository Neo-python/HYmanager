from forms.fields.primary import *
from models.manager import FactoryOrder, Driver
from plugins.HYplugins.form import BaseForm, ListPage, IntegerField, NumberRange
from plugins.HYplugins.form.fields import PhoneField, OrderUuidField, UuidField


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


class OrderEntrustForm(BaseForm, OrderUuidField, UuidField):
    """订单指派/委托给驾驶员"""

    def validate_order_uuid(self, *args):
        """订单编号"""
        self.order = FactoryOrder.query.filter_by(order_uuid=self.order_uuid.data).first()

        if not self.order:
            raise wtforms.ValidationError(message='订单处于无法查询状态.')

    def validate_uuid(self, *args):
        """驾驶员编号"""

        self.driver = Driver.query.filter_by(uuid=self.uuid.data).first()

        if not self.driver:
            raise wtforms.ValidationError(message='驾驶员当前状态无法完成当前业务.')
