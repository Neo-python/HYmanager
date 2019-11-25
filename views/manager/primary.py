from flask import request
from views.manager import api
from forms import manager as forms
from plugins.HYplugins.common.authorization import login
from plugins.HYplugins.common.ordinary import paginate_info, result_format


@api.route('/user/list/')
@login()
def user_list():
    """用户列表"""

    form = forms.UserListForm(request.args).validate_()

    query = form.model.query

    if form.phone.data:
        query = query.filter(f'%{form.phone.data}')

    if form.name.data:
        query = query.filter(f'%{form.name.data}%')

    paginate = query.paginate(form.page.data, form.limit.data, error_out=False)

    data = paginate_info(paginate, items=[item.serialization() for item in paginate.items])

    return result_format(data=data)
