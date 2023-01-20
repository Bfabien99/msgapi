from flask import Blueprint
from flask_bcrypt import Bcrypt
from config import pyConnect
from functions import *
from datetime import datetime

bcrypt = Bcrypt()
users = Blueprint('users', __name__, url_prefix='/users')

########################################
### RECUPERER TOUS LES UTILISATEURS
@users.route('/', methods=['GET'])
def users_home():
    """
    This route is used to get a list of all users in the database.
    
    :return: A JSON response containing a list of all users.
    """
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        cursor.execute("select * from users order by createdAt desc")
        users = cursor.fetchall() or False
        if not users:
            return toJson(200, "No users yet")

        for user in users:
            del user['password']
            
        return toJson(200, "All users", users)
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()

########################################
### RECUPERER UN UTILISATEUR
@users.route('/<int:id>', methods=['GET'])
def users_details(id):
    """
    This route is used to get the details of a single user.
    
    :param id: The ID of the user.
    :return: A JSON response containing the details of the user.
    """
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        cursor.execute("select * from users where id=%s", (id))
        user = cursor.fetchone() or False
        if not user:
            return toJson(404, "User not found")

        del user['password']
        return toJson(200, "User found", user)
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()

########################################
### UPDATE D'UN UTILISATEUR
@users.route('/<int:id>', methods=['PUT'])
def users_update(id):
    """
    This route is used to update the details of a single user.
    Some fields are required in the request body.
    
    :field fullname: The fullname of the user.
    :field username: The username of the user.
    :field email: The email of the user.
    :field password: The password of the user.
    :field img_link: The link related to user's image.
    :field bio: The bio of the user.
    :param id: The ID of the user.
    :return: A JSON response containing the updated details of the user.
    """
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
        
        ### ON VERIFIE SI L'UTILISATEUR EXISTE
        cursor.execute("select * from users where id=%s", (id))
        user = cursor.fetchone() or False
        if not user:
            return toJson(404, "User not found")
        
        ### ON VERIFIE SI L'EMAIL ET L'USERNAME DE L'UTILISATEUR N'EXISTE PAS DEJA
        if user['email'] != email and user['username'] != username:
            cursor.execute("select * from users where username=%s", (username))
            if cursor.fetchone():
                return toJson(409, "Username already exist")
            
            cursor.execute("select * from users where email=%s", (email))
            if cursor.fetchone():
                return toJson(409, "Email already exist")
        
        cursor.execute("update users set fullname=%s, username=%s, email=%s, password=%s, img_link=%s, bio=%s where id=%s", (fullname, username, email, hash_pass, img_link, bio, id))
        if conn.commit():
            return toJson(500, "Oops! Try later")
        
        cursor.execute("select * from users where id=%s", (id))
        user = cursor.fetchone()
        
        del user['password']
        return toJson(201, "Account updated", user)
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()

########################################
### SUPPRESSION UN UTILISATEUR
@users.route('/<int:id>', methods=['DELETE'])
def users_delete(id):
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        cursor.execute("select * from users where id=%s", (id))
        user = cursor.fetchone() or False
        if not user:
            return toJson(404, "User not found")

        cursor.execute("delete from users where id=%s", (id))
        if conn.commit():
            return toJson(500, "Oops! Try later")
        
        return toJson(200, "User deleted")
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()

########################################
### RECUPERER LES ECHANGES ENTRE DEUX UTILISATEURS      
@users.route('/<int:sender_id>/messages/<int:receiver_id>', methods=['GET'])
def users_exchanges(sender_id, receiver_id):
    if sender_id == receiver_id:
        return toJson(401, "You can't send message to yourself")
    
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        
        cursor.execute("select * from users where id=%s", (sender_id))
        sender = cursor.fetchone() or False
        if not sender:
            return toJson(404, "User not found")
        del sender['password']
        
        cursor.execute("select * from users where id=%s", (receiver_id))
        receiver = cursor.fetchone() or False
        if not receiver:
            return toJson(404, "Receiver not found")
        del receiver['password']
        
        cursor.execute(f"select * from messages where (from_id={sender_id} and to_id={receiver_id}) or (from_id={receiver_id} and to_id={sender_id})")
        messages = cursor.fetchall() or False
        if not messages:
            return toJson(200, "No message sent", {'sender':sender, 'receiver':receiver, 'messages':messages})
        
        
        return toJson(200, "All messages", {'sender':sender, 'receiver':receiver, 'messages':messages})
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()

########################################      
### RECUPERER UN MESSAGE DE L'UTILISATEUR
@users.route('/<int:user_id>/messages/<int:message_id>', methods=['GET'])
def users_get_message(user_id, message_id):
    
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        
        cursor.execute("select * from users where id=%s", (user_id))
        user = cursor.fetchone() or False
        if not user:
            return toJson(404, "User not found")
        del user['password']
        
        cursor.execute("select * from messages where msg_id=%s and from_id=%s", (message_id, user_id))
        message = cursor.fetchone() or False
        if not message:
            return toJson(404, "Message not found")
        
        return toJson(200, "Message found", {'user':user, 'messages':message})
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()
        
########################################
### SUPPRIMER UN MESSAGE DE L'UTILISATEUR       
@users.route('/<int:user_id>/messages/<int:message_id>', methods=['DELETE'])
def users_delete_message(user_id, message_id):
    
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        
        cursor.execute("select * from users where id=%s", (user_id))
        user = cursor.fetchone() or False
        if not user:
            return toJson(404, "User not found")
        del user['password']
        
        cursor.execute("select * from messages where msg_id=%s and from_id=%s", (message_id, user_id))
        message = cursor.fetchone() or False
        if not message:
            return toJson(404, "Message not found")
        
        cursor.execute("delete from messages where msg_id=%s", (message_id))
        if conn.commit():
            return toJson(500, "Oops! Try later")
        
        return toJson(200, "Message deleted", {'user':user})
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()

########################################    
### ENVOIE DE MESSAGE D'UN L'UTILISATEUR(SENDER) À UN AUTRE(RECEIVER) 
@users.route('/<int:sender_id>/messageto/<int:receiver_id>', methods=['POST'])
def users_send_message(sender_id, receiver_id):
    if sender_id == receiver_id:
        return toJson(401, "You can't send message to yourself")
    
    received_data = request.get_json()
    required_field = {'content'}
    if isRequired(required_field, received_data):
        return toJson(400, "missing params", isRequired(required_field, received_data))
    
    content = received_data['content'].strip()
    
    try:
        conn = pyConnect()
        cursor= conn.cursor()
        
        cursor.execute("select * from users where id=%s", (sender_id))
        sender = cursor.fetchone() or False
        if not sender:
            return toJson(404, "User not found")
        del sender['password']
        
        cursor.execute("select * from users where id=%s", (receiver_id))
        receiver = cursor.fetchone() or False
        if not receiver:
            return toJson(404, "Receiver not found")
        del receiver['password']
        
        cursor.execute("insert into messages(content, from_id, to_id, sendAt) values(%s, %s, %s, %s)", (content, sender_id, receiver_id, datetime.now()))
        if conn.commit():
            return toJson(500, "Oops! Try later")
        
        return toJson(201, "Message sent")
    except Exception as e:
        return toJson(500, f"Internal server error: {e}")
    finally:
        conn.close()