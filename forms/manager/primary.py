from wtforms.validators import Optional
from forms.fields.primary import *
from models.manager import FactoryOrder
from plugins.HYplugins.form import BaseForm, ListPage, NumberRange
from plugins.HYplugins.form.fields import OrderUuidField, IdSortField
from plugins.HYplugins.form.primary import InputRequired
from plugins.HYplugins.error import ViewException


class DriverListFrom(BaseForm, ListPage):
    """驾驶员列表"""
    verify_status = wtforms.IntegerField(
        default=99
    )


class DriverInfoForm(BaseForm, DriverUUidField):
    """驾驶员详情"""


class DriverOrderListForm(BaseForm, ListPage, DriverUUidField):
    """驾驶员订单列表"""


class DriverReview(BaseForm, DriverUUidField):
    """驾驶员审核"""


class FactoryListFrom(BaseForm, ListPage):
    """厂家列表"""


class FactoryInfoForm(BaseForm, FactoryUUidField):
    """厂家详情"""


class FactoryOrderListForm(BaseForm, ListPage, IdSortField):
    """厂家订单列表"""

    schedule = wtforms.IntegerField(validators=[
        Optional(),
        NumberRange(min=0, max=2, message=VM.say('system_number', 0, 2))
    ],
        default=None
    )

    factory_uuid = wtforms.StringField(validators=[
        Optional(),
        Length(max=40, message=VM.say('system_number', '厂家唯一编号', 30, 40))
    ]
    )

    def validate_factory_uuid(self, *args):
        """厂家编号"""
        self.factory = Factory.query.filter_by(uuid=self.factory_uuid.data).first()

        if not self.factory:
            raise wtforms.ValidationError(message='厂家编号错误')


class FactoryOrderInfoForm(BaseForm, OrderUuidField):
    """厂家订单详情"""

    def validate_order_uuid(self, *args):
        """订单编号"""
        self.order = FactoryOrder.query.filter_by(order_uuid=self.order_uuid.data).first()

        if not self.order:
            raise wtforms.ValidationError(message='订单处于无法查询状态.')
