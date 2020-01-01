import config
from flask import request
from views.manager import api
from forms import manager as forms
from models import Driver, DriverOrder
from plugins import core_api
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common.ordinary import paginate_info, result_format


@api.route('/driver/list/')
@login()
def driver_list():
    """驾驶员列表"""

    form = forms.DriverListFrom(request.args).validate_()

    query = Driver.query

    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    data = paginate_info(paginate, items=[item.serialization() for item in paginate.items])

    return result_format(data=data)


@api.route('/driver/info/')
@login()
def driver_info():
    """驾驶员详情"""

    form = forms.DriverInfoForm(request.args).validate_()

    return result_format(data=form.driver.serialization())


@api.route('/driver/review/pass/')
@login()
def driver_review_pass():
    """同意驾驶员申请"""

    form = forms.DriverReview(request.args).validate_()
    form.driver.verify = 1
    form.driver.direct_update_()
    core_api.clear_token(uuid=form.driver.uuid, port=config.driver_port)
    core_api.send_sms(phone=form.driver.phone, code="申请通过", template_id=config.SMS_TEMPLATE_REGISTERED['review'])
    return result_format()


@api.route('/driver/review/reject/')
@login()
def driver_review_prevent():
    """不同意驾驶员申请"""
    form = forms.DriverReview(request.args).validate_()
    form.driver.verify = -1
    core_api.clear_token(uuid=form.driver.uuid, port=config.driver_port)
    core_api.send_sms(phone=form.driver.phone, code="失败", template_id=config.SMS_TEMPLATE_REGISTERED['review'])
    return result_format()


@api.route('/driver/review/ban/')
@login()
def driver_review_ban():
    """封禁驾驶员"""
    form = forms.DriverReview(request.args).validate_()
    form.driver.verify = -2
    core_api.clear_token(uuid=form.driver.uuid, port=config.driver_port)
    return result_format()


@api.route('/driver/order/list/')
@login()
def driver_order_list():
    """驾驶员订单列表"""
    form = forms.DriverOrderListForm(request.args).validate_()

    query = DriverOrder.query.filter_by(driver_uuid=form.driver.uuid)

    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    data = paginate_info(paginate, items=[item.customize_serialization() for item in paginate.items])

    return result_format(data=data)
