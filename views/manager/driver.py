from flask import request
from views.manager import api
from forms import manager as forms
from models import Driver
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
