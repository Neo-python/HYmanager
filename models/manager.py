from .HYModels import user
from .HYModels import business


class Factory(user.FactoryBase):
    """厂家"""


class Driver(user.DriverBase):
    """驾驶员"""


class FactoryOrder(business.OrderBase):
    """厂家订单"""


class OrderEntrust(business.OrderEntrustBase):
    """订单委托"""
