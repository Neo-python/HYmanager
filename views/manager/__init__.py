"""业务层"""
from flask import Blueprint

api = Blueprint('manager', __name__)

from views.manager.primary import *
from views.manager.business import *
