from flask import Blueprint
from config import pyConnect
from functions import *

main = Blueprint('main', __name__, url_prefix='/')

@main.route('', methods=['GET'])
def main_home():
    return toJson(200, "main's route", {"Main":True})