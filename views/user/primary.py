import time
import uuid
from flask import g
from init import sms, Redis
from views.user import api
from plugins.HYplugins.common import result_format
from plugins.HYplugins.common.authorization import login, auth
from models.system import Admin
from forms import user as forms


@api.route('/sign_in/', methods=['POST'])
def sign_in():
    """登录"""
    # open_id = wechat_api.get_open_id()
    open_id = 'xxxneoxxx1'
    #
    user = Admin.query.filter_by(open_id=open_id).first()
    #
    if user:  # 用户信息存在
        return result_format(data={'token': user.generate_token(), 'user_info': user.serialization()})
    else:
        return result_format(error_code=4001, message='管理员不存在', data={'open_id': open_id})


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
        return result_format(error_code=4008, message='token刷新失败,有效期还长着呢.')


@api.route('/activation/', methods=['POST'])
def activation():
    """激活成为管理员
    激活成功后删除Redis中的短信验证码信息
    :return:
    """

    form = forms.ActivationForm().validate_()

    form.admin.open_id = form.open_id.data
    form.admin.name = form.name.data
    form.admin.uuid = uuid.uuid1().hex
    form.admin.sms_status = False
    form.admin.update_create_time()
    form.admin.direct_update_()

    Redis.delete(form.redis_key)
    return result_format()


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
