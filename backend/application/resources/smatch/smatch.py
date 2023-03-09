from flask import Blueprint
from orm_interface.base import Session
from orm_interface.entities.user import User

smatch = Blueprint("smatch", __name__)
session = Session()

def get_user(username):
    
    # cur.execute('SELECT id, username, password FROM users WHERE username = %s', (username,))
    user = session.query(User).filter(User.email == username).first()

    if user is None:
        return None
    
    return user

def get_user_by_id(id):
    
    # cur.execute('SELECT id, username, password FROM users WHERE id = %s', (id,))
    user = session.query(User).filter(User.id == id).first()

    return user

@smatch.route("/home")
@smatch.route("/")
def smatch_home():
    return "Smatch home"