import time
import uuid
from flask import g
from views import Admin
from views.user import api
from plugins import Redis
from plugins.HYplugins.common import result_format
from plugins.HYplugins.common.authorization import login, auth
from forms import user as forms


@api.route('/sign_in/', methods=['POST'])
def sign_in():
    """登录"""
    form = forms.SignInForm().validate_()

    user = Admin.query.filter_by(open_id=form.open_id).first()

    if user:

        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(error_code=5011, message='客户未注册')


@api.route('/refresh_token/')
@auth.login_required
def refresh_token():
    """刷新token"""

    day = 20

    iat = g.user.get('iat')

    if time.time() - time.mktime(time.localtime(iat)) > (60 * 60 * 24 * day):
        user = Admin.query.filter_by(uuid=g.user.uuid).first_or_404()
        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(error_code=5009, message='token刷新失败.')


@api.route('/activation/', methods=['POST'])
def activation():
    """激活成为管理员
    激活成功后删除Redis中的短信验证码信息
    :return:
    """

    form = forms.ActivationForm().validate_()

    form.admin.open_id = form.open_id
    form.admin.name = form.name.data
    form.admin.uuid = uuid.uuid1().hex
    form.admin.sms_status = False
    form.admin.update_create_time()
    form.admin.direct_update_()

    Redis.delete(form.redis_key)
    return result_format(data={'token': form.admin.generate_token(), 'user_info': form.admin.serialization()})


@api.route('/info/')
@login()
def admin_info():
    """管理员信息查询"""
    user = Admin.query.filter_by(uuid=g.user.uuid).first_or_404()
    return result_format(data=user.serialization())


@api.route('/info/edit/', methods=['POST'])
@login()
def admin_info_edit():
    """管理员信息修改"""
    form = forms.AdminInfoEditForm().validate_()
    user = Admin.query.filter_by(uuid=g.user.uuid).first_or_404()
    user.set_attrs(form.data).direct_update_()
    return result_format()


@api.route('/system/notice/set/', methods=['POST'])
@login()
def admin_system_notice():
    """管理员短信通知设置"""
    form = forms.AdminSystemNoticeForm().validate_()
    user = Admin.query.filter_by(uuid=g.user.uuid).first_or_404()
    if form.options == 1:
        user.sms_status = True
    else:
        user.sms_status = False
    user.direct_update_()
    return result_format()
