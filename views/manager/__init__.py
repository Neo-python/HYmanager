"""业务层"""
from flask import Blueprint

api = Blueprint('manager', __name__)

from views.manager.business import *
from views.manager.driver import *
from views.manager.factory import *
