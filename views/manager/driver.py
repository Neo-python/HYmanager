import config
from flask import request, g
from views.manager import api
from forms import manager as forms
from models import Driver
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
    user = g.user
    form.driver.verify = 1
    form.driver.remark = f'由"{user.name}"通过认证'
    core_api.clear_token(uuid=form.driver.uuid, port=config.driver_port)
    return result_format()


@api.route('/driver/review/reject/')
@login()
def driver_review_prevent():
    """不同意驾驶员申请"""
    form = forms.DriverReview(request.args).validate_()
    user = g.user
    form.driver.verify = -1
    form.driver.remark = f'由"{user.name}"驳回'
    core_api.clear_token(uuid=form.driver.uuid, port=config.driver_port)
    return result_format()


@api.route('/driver/review/ban/')
@login()
def driver_review_ban():
    """封禁驾驶员"""
