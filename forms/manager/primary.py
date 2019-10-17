from forms.fields.primary import *
from plugins.HYplugins.form import BaseForm, ListPage
from plugins.HYplugins.form.fields import PhoneField


class UserListForm(BaseForm, UserGenreField, ListPage):
    """用户列表"""

    phone = wtforms.StringField(validators=[
        Optional(),
        Length(max=11, message=VM.say('length', '手机号', 1, 11))
    ])

    name = wtforms.StringField(validators=[
        Optional(),
        Length(max=10, message=VM.say('length', '名称', 1, 10))
    ])
