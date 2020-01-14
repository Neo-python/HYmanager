import config
from flask import g, request
from views.manager import api
from forms import manager as forms
from models.manager import FactoryOrder
from plugins import core_api
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common.ordinary import result_format, paginate_info


@api.route('/order/info/')
@login()
def order_info():
    """订单详情"""

    form = forms.FactoryOrderInfoForm(request.args).validate_()

    return result_format(data=form.order.serialization(remove={"id"}))
