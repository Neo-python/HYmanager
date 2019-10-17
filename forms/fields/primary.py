import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class AdminNameField:
    """管理员姓名"""
    name = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '管理员姓名')),
        Length(max=10, message=VM.say('length', '管理员姓名', 1, 10))
    ])
