from wtforms.validators import Optional
from forms.fields.primary import *
from models.manager import FactoryOrder, Driver, OrderEntrust
from plugins.HYplugins.form import BaseForm, ListPage, NumberRange, JsonField
from plugins.HYplugins.form.fields import OrderUuidField, IdSortField
from plugins.HYplugins.error import ViewException


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


class FactoryOrderListForm(BaseForm, ListPage, IdSortField):
    """厂家订单列表"""

    entrust_status = wtforms.IntegerField(validators=[
        Optional(),
        NumberRange(min=0, max=2, message=VM.say('system_number', 0, 2))
    ],
        default=0
    )


class OrderEntrustForm(BaseForm, OrderUuidField):
    """订单指派/委托给驾驶员"""

    driver_list = JsonField(validators=[DataRequired(message=VM.say('required', '驾驶员名单'))])

    def validate_order_uuid(self, *args):
        """订单编号
        检查订单编号时候存在
        检查订单是否已被接单
        """
        self.order = FactoryOrder.query.filter_by(order_uuid=self.order_uuid.data).first()

        if not self.order:
            raise wtforms.ValidationError(message='订单处于无法查询状态.')
        entrust = OrderEntrust.query.filter_by(order_uuid=self.order.order_uuid, entrust_status=1).first()
        if entrust:
            raise ViewException(error_code=5110,
                                message=f'订单已被"{entrust.driver.name},{entrust.driver.phone}"接走,请先与该驾驶员取得联系')

    def validate_driver_list(self, *args):
        """驾驶员编号"""

        self.driver_list = Driver.query.filter(Driver.uuid.in_(self.driver_list.data)).all()



class OrderInfoForm(BaseForm, OrderUuidField):
    """订单详情"""

    def validate_order_uuid(self, *args):
        """订单编号"""
        self.order = FactoryOrder.query.filter_by(order_uuid=self.order_uuid.data).first()

        if not self.order:
            raise wtforms.ValidationError(message='订单处于无法查询状态.')
