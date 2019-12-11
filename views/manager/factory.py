from flask import request
from views.manager import api
from forms import manager as forms
from models import Factory, FactoryOrder
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common.ordinary import paginate_info, result_format


@api.route('/factory/list/')
@login()
def factory_list():
    """厂家列表"""
    form = forms.FactoryListFrom(request.args).validate_()

    query = Factory.query

    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    data = paginate_info(paginate, items=[item.serialization() for item in paginate.items])

    return result_format(data=data)


@api.route('/factory/info/')
@login()
def factory_info():
    """厂家详情"""

    form = forms.FactoryInfoForm(request.args).validate_()

    return result_format(data=form.factory.serialization())


@api.route('/factory/order/list/')
@login()
def factory_order_list():
    """厂家订单列表"""
    form = forms.FactoryOrderListForm(request.args).validate_()

    query = FactoryOrder.query

    if form.factory_uuid.data:
        query = query.filter_by(factory_uuid=form.factory.uuid)

    if form.schedule.data is not None:
        query = query.filter_by(schedule=form.schedule.data)

    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    data = paginate_info(paginate, items=[item.serialization() for item in paginate.items])

    return result_format(data=data)
