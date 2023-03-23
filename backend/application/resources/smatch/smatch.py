from flask import Blueprint, jsonify
from orm_interface.base import Session
from orm_interface.entities.user import User
from orm_interface.entities.smatch.smatch_courselist import Smatch_CourseList

from flask_jwt_extended import get_jwt_identity, JWTManager, jwt_required

smatch = Blueprint("smatch", __name__)
session = Session()

jwt_mng = JWTManager()

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
@jwt_required()
def smatch_home():
    user_data = get_jwt_identity()

    return f"Smatch home, {user_data['id']}, {user_data['email']}, {user_data['firstname']}, {user_data['lastname']}"


@smatch.route('/topics')
def list_topics():
    # cur.execute('SELECT DISTINCT category FROM courselist ORDER BY category ASC')
    categories = session.query(Smatch_CourseList.category.distinct())\
        .order_by(Smatch_CourseList.category).all()

    topics = list()
    for (name,) in categories:
        topics.append(name)
    
    return jsonify(topics)