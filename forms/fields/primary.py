import wtforms
from wtforms.validators import DataRequired, Length
from models.manager import Factory, Driver
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class AdminNameField:
    """管理员姓名"""
    name = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '管理员姓名')),
        Length(max=10, message=VM.say('length', '管理员姓名', 1, 10))
    ])


class UserGenreField:
    """用户类型"""

    models = {
        'factory': Factory,
        'driver': Driver
    }

    user_genre = wtforms.SelectField(validators=[
        DataRequired(message=VM.say('required', '用户类型'))
    ],
        choices=[('factory', 'factory'), ('driver', 'driver')]
    )

    def validate_user_genre(self, *args):
        """验证用户类型"""
        try:
            self.model = self.models[self.user_genre.data]
        except Exception as err:
            raise wtforms.ValidationError(message='用户的类型输入错误')
