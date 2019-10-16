from forms.fields.primary import *
from plugins.HYplugins.form import BaseForm
from plugins.HYplugins.form.fields import PhoneField


class SMSCodeForm(BaseForm, PhoneField):
    """短信发送表单"""
    genre = wtforms.SelectField(validators=[DataRequired()],
                                choices=[('registered', 'registered'), ('edit_phone', 'edit_phone')])
