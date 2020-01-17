import wtforms
from wtforms.validators import DataRequired, Length
from models import Factory, Driver
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class DriverUUidField:
    """驾驶员编号"""

    driver_uuid = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '驾驶员唯一编号')),
        Length(max=40, message=VM.say('system_number', '驾驶员唯一编号', 30, 40))
    ]
    )

    def validate_driver_uuid(self, *args):
        """驾驶员唯一编号"""
        self.driver = Driver.query.filter_by(uuid=self.driver_uuid.data).first()

        if not self.driver:
            raise wtforms.ValidationError(message='驾驶员编号错误')


class FactoryUUidField:
    """厂家编号"""

    factory_uuid = wtforms.StringField(validators=[
        DataRequired(message=VM.say('required', '厂家唯一编号')),
        Length(max=40, message=VM.say('system_number', '厂家唯一编号', 30, 40))
    ]
    )

    def validate_factory_uuid(self, *args):
        """厂家编号"""
        self.factory = Factory.query.filter_by(uuid=self.factory_uuid.data).first()

        if not self.factory:
            raise wtforms.ValidationError(message='厂家编号错误')


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
