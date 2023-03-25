import pandas as pd
from sqlalchemy import create_engine

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.cluster import KMeans
from orm_interface.entities.smatch.smatch_courselist import Smatch_CourseList

from orm_interface.base import Session

session = Session()

def get_all_courses(filters):
    # query = "SELECT * FROM courselist WHERE category = %s AND price >= %s AND price <= %s AND duration >= %s AND duration <= %s AND level IN %s"
    # params = (filters["category"], filters["price_min"], filters["price_max"], filters["duration_min"], filters["duration_max"], tuple(filters["levels"]))
    # courses = pd.read_sql_query(query, con=engine, params=params)

    levels = tuple(filters["levels"])
    courses = session.query(Smatch_CourseList).filter(Smatch_CourseList.category == filters["category"], Smatch_CourseList.price >= filters["price_min"],
        Smatch_CourseList.price <= filters["price_max"], Smatch_CourseList.duration >= filters["duration_min"], Smatch_CourseList.duration <= filters["duration_max"],
        Smatch_CourseList.level.in_(levels)).all()

    return courses

def kmeans(courses):
    # Represent each article as a vector
    my_stop_words = text.ENGLISH_STOP_WORDS.union(
        ["learn", "digital", "online", "specialization", "course", "platform", "courses"])
    vectorizer = TfidfVectorizer(ngram_range=(1, 1), stop_words=my_stop_words)
    X = vectorizer.fit_transform(courses.description)

    # Chosen based on the elbow method
    true_k = 8
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
    model.fit(X)
    labels = model.labels_
    result = pd.DataFrame(list(zip(courses.name, courses.id, labels)), columns=['subject', 'course_id', 'cluster'])

    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    terms_df = pd.DataFrame(columns=["cluster", "text"])
    for i in range(true_k):
        termz = []
        for ind in order_centroids[i, :100]:
            blob = terms[ind]
            termz += [blob]
        dicti = {
            "cluster": i,
            "text": termz
        }
        terms_df = terms_df.append(dicti, ignore_index=True)

    return result, terms_df

def make_clusters(filters):
    courses = get_all_courses(filters)
    (clusters, terms) = kmeans(courses)
    return (clusters, terms)