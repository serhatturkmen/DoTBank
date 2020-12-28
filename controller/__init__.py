from flask import Blueprint

controllerBlueprint = Blueprint('controller', __name__)

from . import homeController
from .api import apiController

