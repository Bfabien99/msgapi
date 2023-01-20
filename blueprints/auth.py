from flask import Blueprint, request
from flask_bcrypt import Bcrypt
from config import pyConnect
from functions import *
from datetime import datetime

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/', methods=['GET'])
def auth_home():
    return toJson(200, "authentification's route", {"Authentification":True})

#### LOGIN USERS
@auth.route('/login', methods=['POST'])
def auth_login():
    received_data = request.get_json()
    required_field = {'username', 'email', 'password'}
    if isRequired(required_field, received_data):
        return toJson(400, "missing params", isRequired(required_field, received_data))
    
    username = received_data['username'].lower().strip()
    email = received_data['email'].lower().strip()
    password = received_data['password'].strip()
    
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        cursor.execute("select * from users where username=%s and email=%s", (username, email))
        user = cursor.fetchone() or False
        if not user or not bcrypt.check_password_hash(user['password'], password):
            return toJson(403, "Invalid credentials")
        
        del user['password']
        return toJson(200, "Login successfully", user)
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()

#### SIGNUP USERS
@auth.route('/signup', methods=['POST'])
def auth_signup():
    received_data = request.get_json()
    required_field = {'fullname', 'username', 'email', 'password', 'img_link', 'bio'}
    if isRequired(required_field, received_data):
        return toJson(400, "missing params", isRequired(required_field, received_data))
    
    fullname = received_data['fullname'].lower().strip()
    username = received_data['username'].lower().strip()
    email = received_data['email'].lower().strip()
    password = received_data['password'].strip()
    img_link = received_data['img_link']
    bio = received_data['bio']
    
    hash_pass = bcrypt.generate_password_hash(password=password)
    
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        cursor.execute("select * from users where username=%s or email=%s", (username, email))
        if cursor.fetchone():
            return toJson(409, "User already exist")
        
        cursor.execute("insert into users(fullname, username, email, password, img_link, bio, createdAt) values(%s, %s, %s, %s, %s, %s, %s)", (fullname, username, email, hash_pass, img_link, bio, datetime.utcnow()))
        if conn.commit():
            return toJson(500, "Oops! Try later")
        
        cursor.execute("select * from users where username=%s", (username))
        user = cursor.fetchone()
        
        return toJson(201, "Account created", user)
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()
    