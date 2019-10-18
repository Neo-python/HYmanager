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
    """厂家订单列表"""

    form = forms.FactoryOrderListForm(request.args).validate_()
    query = FactoryOrder.query
    if form.create_time_sort is not None:
        if form.create_time_sort.data == 0:
            query = query.order_by(FactoryOrder.create_time.desc())

    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    data = paginate_info(paginate, items=[item.serialization() for item in paginate.items])

    return result_format(data=data)


@api.route('/order/entrust/', methods=['POST'])
@login()
def order_entrust():
    """订单指派/委托给驾驶员"""

    form = forms.OrderEntrustForm().validate_()

    for driver in form.driver_list:
        OrderEntrust(order_uuid=form.order.order_uuid, driver_uuid=driver.uuid).direct_add_()

    OrderEntrust.static_commit_()

    core_api.send_sms()