import config
from flask import g, request
from views.manager import api
from init import core_api
from forms import manager as forms
from models.manager import FactoryOrder, OrderEntrust
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common.ordinary import result_format, paginate_info


@api.route('/factory/order/list/')
@login()
def factory_order_list():
    """厂家订单列表
    1. 过滤订单委托状态
        0:未被委托的订单
        1:已被委托的订单
        2:委托后被接单的订单
    """

    form = forms.FactoryOrderListForm(request.args).validate_()

    query = FactoryOrder.query

    # 过滤订单委托状态.
    query = query.join(OrderEntrust, isouter=True)
    if form.entrust_status.data == 0:
        query = query.filter(OrderEntrust.order_uuid.is_(None))
    elif form.entrust_status.data == 1:
        query = query.filter(FactoryOrder.order_uuid == OrderEntrust.order_uuid, OrderEntrust.entrust_status == 0)
    elif form.entrust_status.data == 2:
        query = query.filter(FactoryOrder.order_uuid == OrderEntrust.order_uuid, OrderEntrust.entrust_status == 1)

    if form.create_time_sort is not None:
        if form.create_time_sort.data == 0:
            query = query.order_by(FactoryOrder.id.desc())

    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    data = paginate_info(paginate, items=[item.serialization(remove={"id"}) for item in paginate.items])

    return result_format(data=data)


@api.route('/order/entrust/', methods=['POST'])
@login()
def order_entrust():
    """订单指派/委托给驾驶员
    检查订单
    校验驾驶员编号
    剔除已经被委托的驾驶员,避免重复委托
    """

    form = forms.OrderEntrustForm().validate_()
    user = g.user

    entrusts = OrderEntrust.query.filter(order_uuid=form.order.order_uuid).all()
    entrusts_driver_list = [item.driver_uuid for item in entrusts]  # 已被委托的驾驶员列表

    for driver in form.driver_list:
        if driver not in entrusts_driver_list:  # 剔除已经被委托的驾驶员,避免重复委托
            OrderEntrust(order_uuid=form.order.order_uuid, driver_uuid=driver.uuid,
                         managers_uuid=user.uuid).direct_add_()

    OrderEntrust.static_commit_()

    # 通知驾驶员接单短信
    core_api.batch_sms(template_id=config.SMS_TEMPLATE_REGISTERED['order_entrust'],
                       phone_list=[driver.phone for driver in form.driver_list],
                       params=[form.order.order_uuid]
                       )
    return result_format()


@api.route('/order/info/')
@login()
def order_info():
    """订单详情"""

    form = forms.OrderInfoForm(request.args).validate_()

    return result_format(data=form.order.serialization(remove={"id"}))
