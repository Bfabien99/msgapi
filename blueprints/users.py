from flask import Blueprint
from config import pyConnect
from functions import *

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['GET'])
def users_home():
    return toJson(200, "users's route", {"Users":True})