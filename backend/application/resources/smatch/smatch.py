from datetime import datetime

from flask import Blueprint, jsonify, request, abort
from orm_interface.base import Session
from orm_interface.entities.user import User
from orm_interface.entities.smatch.smatch_courselist import Smatch_CourseList

from orm_interface.entities.smatch.smatch_threads import Smatch_Thread
from orm_interface.entities.smatch.smatch_replies import Smatch_Reply
from orm_interface.entities.smatch.smatch_matched_terms import Smatch_MatchedTerm
from orm_interface.entities.smatch.smatch_history import Smatch_History

from flask_jwt_extended import get_jwt_identity, JWTManager, jwt_required

from .recommender import make_clusters

import json

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
        .filter(Smatch_CourseList.category != '-') \
        .order_by(Smatch_CourseList.category).all()

    topics = list()
    for (name,) in categories:
        topics.append(name)

    topics.sort()

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

    results_dict = [dict(row) for row in results]
    
    return jsonify(results_dict)



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

    thread = {
        'id': thread.Smatch_Thread.id,
        'user_id': thread.Smatch_Thread.user_id,
        'title': thread.Smatch_Thread.title,
        'body': thread.Smatch_Thread.body,
        'created_on': thread.Smatch_Thread.created_on,
        'category': thread.Smatch_Thread.category,
        'email': thread.email,
        'replies': [
            {
                'id': reply.Smatch_Reply.id,
                'user_id': reply.Smatch_Reply.user_id,
                'body': reply.Smatch_Reply.body,
                'created_on': reply.Smatch_Reply.created_on,
                'email': reply.email,
            } for reply in replies
        ]
    }

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
    new_item = Smatch_Thread(title=title, created_on=datetime.now(), category=category, body=body, user_id=user_id)
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


# Add new replies on the thread with thread_id
@smatch.route('/threads/<thread_id>/replies', methods = ['POST'])
@jwt_required()
def new_reply(thread_id):
    user_id = get_jwt_identity()['id']

    body = request.json.get('body')

    # cur.execute('INSERT INTO replies (user_id, thread_id, body) VALUES (%s, %s, %s)', (user.id, thread_id, body))
    new_item = Smatch_Reply(user_id=user_id, created_on=datetime.now(), thread_id=thread_id, body=body)
    session.add(new_item)

    try:
        session.commit()
        return {}, 201
    except Exception as e :
        print(str(e))
        session.rollback()
    finally:
        session.close()
    
    abort(400)





visualization_queries = {
    "instructors": "SELECT count(*), instructor FROM smatch_courselist WHERE instructor IS NOT NULL GROUP BY instructor ORDER BY count DESC LIMIT 20",
    "providers": "SELECT count(*), provider FROM smatch_courselist WHERE provider IS NOT NULL GROUP BY provider ORDER BY count DESC LIMIT 20",
    "categories": "SELECT count(*), coalesce(category, 'Other') category FROM smatch_courselist GROUP BY category ORDER BY count DESC LIMIT 20",
    "levels": "SELECT count(*), level FROM smatch_courselist GROUP BY level ORDER BY count DESC",
    "duration_-": "SELECT count(*), duration FROM smatch_courselist WHERE duration IS NOT NULL GROUP BY duration ORDER BY count DESC",
    "duration_Beginner": "SELECT count(*), duration FROM smatch_courselist WHERE duration IS NOT NULL AND level = 'Beginner' GROUP BY duration ORDER BY count DESC",
    "duration_Intermediate": "SELECT count(*), duration FROM smatch_courselist WHERE duration IS NOT NULL AND level = 'Intermediate' GROUP BY duration ORDER BY count DESC",
    "duration_Advanced": "SELECT count(*), duration FROM smatch_courselist WHERE duration IS NOT NULL AND level = 'Advanced' GROUP BY duration ORDER BY count DESC",
    "duration_All": "SELECT count(*), duration FROM smatch_courselist WHERE duration IS NOT NULL AND level = 'All' GROUP BY duration ORDER BY count DESC",
    "price_-": "SELECT count(*), price FROM smatch_courselist WHERE price IS NOT NULL GROUP BY price ORDER BY count DESC",
    "price_Beginner": "SELECT count(*), price FROM smatch_courselist WHERE price IS NOT NULL AND level = 'Beginner' GROUP BY price ORDER BY count DESC",
    "price_Intermediate": "SELECT count(*), price FROM smatch_courselist WHERE price IS NOT NULL AND level = 'Intermediate' GROUP BY price ORDER BY count DESC",
    "price_Advanced": "SELECT count(*), price FROM smatch_courselist WHERE price IS NOT NULL AND level = 'Advanced' GROUP BY price ORDER BY count DESC",
    "price_All": "SELECT count(*), price FROM smatch_courselist WHERE price IS NOT NULL AND level = 'All' GROUP BY price ORDER BY count DESC",
    "terms": "SELECT * FROM smatch_matched_terms ORDER BY count DESC LIMIT 50"
};

@smatch.route('/visualization/<name>')
@jwt_required()
def visualization(name):
    # cur.execute(visualization_queries[name])
    # result = cur.fetchall()
    result = session.execute(visualization_queries[name]).fetchall()
    return jsonify(result)


@smatch.route('/current_user')
@jwt_required()
def current_user():
    #user = auth.current_user()
    user_id = get_jwt_identity()['id']
    user = session.query(User).filter(User.id == user_id).first()
    user['username'] = user['email']
    return jsonify(user)

@smatch.route('/current_user', methods = ['POST'])
@jwt_required()
def update_username():
    user_id = get_jwt_identity()['id']

    username = request.json.get('username')

    user = session.query(User).filter(User.email == username).first()

    if user:
        user['email'] = username

        try:
            session.commit()
            return {}
        except Exception as e :
            print(str(e))
            session.rollback()
        finally:
            session.close()
    
    abort(400)


@smatch.route('/generate_clusters', methods = ['POST'])
@jwt_required()
def generate_clusters():
    filters = request.json
    (clusters, terms) = make_clusters(filters)
    return jsonify({ "clusters": clusters.to_dict('records'), "terms": terms.to_dict('records') })


@smatch.route('/course/<id>')
@jwt_required()
def get_course(id):
    # cur.execute('SELECT * FROM courselist WHERE id = %s', (id,))
    course = session.query(Smatch_CourseList).filter(Smatch_CourseList.id == id).first()

    if course:
        course = {
            'id': course.id,
            'name': course.name,
            'provider': course.provider,
            'level': course.level,
            'instructor': course.instructor,
            'description': course.description,
            'duration': course.duration,
            'price': course.price,
            'link': course.link,
            'category': course.category
        }

        return jsonify(course)
    
    abort(404)


@smatch.route('/swiped_terms', methods = ['POST'])
@jwt_required()
def swiped_terms():
    terms = request.json.get('terms')

    try:
        for term in terms:
            print('Term:', term)
            # cur.execute('INSERT INTO matched_terms (term, count) VALUES (%s, 1) ON CONFLICT (term) DO UPDATE SET count = matched_terms.count + 1', (term,))
            sel_term_item = session.query(Smatch_MatchedTerm).filter(Smatch_MatchedTerm.term == str(term)).first()

            if sel_term_item:
                sel_term_item.count += 1
                session.commit()
            else:
                new_term = Smatch_MatchedTerm(term=term, count=1)
                session.add(new_term)
                session.commit()
                session.refresh(new_term)

        return jsonify({}), 201
    
    except:
        abort(400)


@smatch.route('/store_suggestion', methods = ['POST'])
@jwt_required()
def store_suggestion():
    user_id = get_jwt_identity()['id']
    
    result = request.json
    
    topic = result['topic']
    suggestions = json.dumps(result['suggestions'])

    
    new_item = Smatch_History(user_id=user_id, topic=topic, result=suggestions, created_on=datetime.now())
    session.add(new_item)
    
    try:
        session.commit()
        return jsonify({}), 201
    except Exception as e :
        print(str(e))
        session.rollback()
    finally:
        session.close()

    abort(400)
    
    
@smatch.route('/get_history')
@jwt_required()
def get_history():
    user_id = get_jwt_identity()['id']
    
    histories = session.query(Smatch_History).filter(Smatch_History.user_id == user_id) \
        .order_by(Smatch_History.created_on.desc()).all()
        
    
    histories = [
        {
            'id': item.id,
            'topic': item.topic,
            'result': item.result,
            'created_on': item.created_on,
        } for item in histories]
    
    return jsonify(histories)