from models.HYModels import user
from models.HYModels import business


class Factory(user.FactoryBase):
    """厂家"""


class Driver(user.DriverBase):
    """驾驶员"""


class DriverSystemMessage(user.DriverSystemMessageBase):
    """驾驶员系统消息"""


class FactoryOrder(business.OrderBase):
    """厂家订单"""
