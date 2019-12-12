from wtforms.validators import Optional
from forms.fields.primary import *
from models.manager import FactoryOrder, Driver
from plugins.HYplugins.form import BaseForm, ListPage, NumberRange, JsonField
from plugins.HYplugins.form.fields import OrderUuidField, IdSortField
from plugins.HYplugins.error import ViewException


class DriverListFrom(BaseForm, ListPage):
    """驾驶员列表"""


class DriverInfoForm(BaseForm, DriverUUidField):
    """驾驶员详情"""


class DriverReview(BaseForm, DriverUUidField):
    """驾驶员审核"""


class FactoryListFrom(BaseForm, ListPage):
    """厂家列表"""


class FactoryInfoForm(BaseForm, FactoryUUidField):
    """厂家详情"""


# class UserListForm(BaseForm, UserGenreField, ListPage):
#     """用户列表"""
#
#     phone = wtforms.StringField(validators=[
#         Optional(),
#         Length(max=11, message=VM.say('length', '手机号', 1, 11))
#     ])
#
#     name = wtforms.StringField(validators=[
#         Optional(),
#         Length(max=10, message=VM.say('length', '名称', 1, 10))
#     ])


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
        Length(min=39, max=39, message=VM.say('length_unite', '厂家唯一编号', 39))
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
