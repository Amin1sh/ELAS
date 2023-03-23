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
@jwt_required()
def list_topics():
    # cur.execute('SELECT DISTINCT category FROM courselist ORDER BY category ASC')
    categories = session.query(Smatch_CourseList.category.distinct())\
        .order_by(Smatch_CourseList.category).all()

    topics = list()
    for (name,) in categories:
        topics.append(name)
    
    return jsonify(topics)



#This access the database of all the threads
@smatch.route("threads")
@jwt_required()
def smatch_threads():

    results = session.execute('''WITH reply_count AS (SELECT thread_id, count(id) FROM smatch_replies GROUP BY thread_id),
     last_reply AS (SELECT thread_id, max(created_on) FROM smatch_replies GROUP BY thread_id)
    SELECT smatch_threads.*, email, coalesce(reply_count.count, 0) replies, coalesce(last_reply.max, created_on) AS last_reply_on
    FROM smatch_threads
    JOIN "user" ON smatch_threads.user_id = "user".id
    LEFT OUTER JOIN reply_count ON smatch_threads.id = reply_count.thread_id
    LEFT OUTER JOIN last_reply ON smatch_threads.id = last_reply.thread_id
    ORDER BY last_reply_on DESC
    ''').fetchall()
    
    return jsonify(results)



# this shows the replies for a specific thread
@smatch.route('/threads/<thread_id>')
@jwt_required()
def show_replies(thread_id):
    # cur.execute('SELECT threads.*, username FROM threads JOIN users ON threads.user_id = users.id WHERE threads.id = %s', (int(thread_id),))
    # thread = cur.fetchone()
    thread = session.query(Smatch_Thread, User.email).join(User, Smatch_Thread.user_id == User.id).filter(Smatch_Thread.id == int(thread_id)).first()

    if not thread:
        abort(404)

    #cur.execute('SELECT replies.*, username FROM replies JOIN users ON replies.user_id = users.id WHERE replies.thread_id = %s ORDER BY created_on ASC', (int(thread_id),))
    #replies = cur.fetchall()
    replies = session.query(Smatch_Reply, User.email).join(User, Smatch_Reply.user_id == User.id).filter(Smatch_Reply.thread_id == int(thread_id)).order_by(Smatch_Reply.created_on).all()

    thread['replies'] = replies

    return jsonify(thread)


@smatch.route('/user_count')
@jwt_required()
def user_count():
    # cur.execute('SELECT count(*) FROM users')
    # user_count = cur.fetchone()
    user_count = session.query(User).count()
    return jsonify(user_count)



# Add new threads
@smatch.route('/threads', methods = ['POST'])
@jwt_required()
def new_thread():
    user_id = get_jwt_identity()['id']
    
    title = request.json.get('title')
    category = request.json.get('category')
    body = request.json.get('body')

    # cur.execute('INSERT INTO threads (user_id, title, category, body) VALUES (%s, %s, %s, %s) RETURNING id', (user.id, title, category, body))
    new_item = Smatch_Thread(title=title, category=category, body=body,user_id=user_id)
    session.add(new_item)

    try:
        # conn.commit()
        session.commit()

        return { "thread_id": new_item.id }, 201
    except Exception as e :
        print(str(e))
        session.rollback()
    finally:
        session.close()
    
    abort(400)