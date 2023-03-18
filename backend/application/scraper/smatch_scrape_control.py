import pandas as pd
import requests, json

import os
import yaml
from datetime import datetime

import pandas as pd
import numpy as np
import json
import nltk
import re
import csv
import matplotlib.pyplot as plt 
import seaborn as sns
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB


# for add in database
from orm_interface.base import Session
from orm_interface.entities.smatch.smatch_courselist import Smatch_CourseList
session = Session()


def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip(' ')
    return text

def labeling_process(data):
    unlabeled = data[data.category.isnull()]
    labeled = data[data.category.notnull()]

    available_cat = list(dict.fromkeys(labeled["category"]))
    print('Available Categories:', available_cat)

    labeled['description'] = labeled['description'].map(lambda com : clean_text(com))
    unlabeled['description'] = unlabeled['description'].map(lambda com : clean_text(com))

    X_train =labeled.name
    X_test = unlabeled.name
    y_train = labeled.category

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, y_train)

    clf.predict((count_vect.transform(["This course begins with a look at the determinants of value. We will cover two main approaches to valuing businesses as going concerns, discounting cash flows and valuation ratios, including the inputs needed to perform the calculations and how each deal with risk."])))[0]

    data['clean_name'] = data['name'].map(lambda com : clean_text(com))
    data['category'] = data['category'].fillna("a")
    print(data)
    for index,row in data.iterrows():
        if row["category"] == "a":
            try:
                data.loc[index,"category"] = clf.predict((count_vect.transform([row["clean_name"]])))[0]
                print(data.loc[index,"category"])
            except:
                pass

    data = data.loc[:, ~data.columns.str.contains('clean_name')]
    return data

### --------------- Udemy section -------------------
client_ID = "FPjQAWG0Dd4vejVo6Tu1jurZoamF1zQbOob0k8Q7"
client_secret = "wLo0LigtQI1KyUHCVNbKpgLY9vYZchySspzYAwqAn8mMnxzpdWMUmV5eP7sw8GLI38X0EMlT5N3ZENzgTpvK7CGVoNI3RR88eZ0GF6ssJvlrZNi34MbhVUCj6VUYq4wq"


client_id_secret = f"{client_ID}:{client_secret}"

#b64_client_id_secret = base64.b64encode(client_id_secret)


s = requests.session()
s.headers = {'Authorization': 'Basic RlBqUUFXRzBEZDR2ZWpWbzZUdTFqdXJab2FtRjF6UWJPb2IwazhRNzp3TG8wTGlndFFJMUt5VUhDVk5iS3BnTFk5dllaY2h5U3NwellBd3FBbjhtTW54enBkV01VbVY1ZVA3c3c4R0xJMzhYMEVNbFQ1TjNaRU56Z1Rwdks3Q0dWb05JM1JSODhlWjBHRjZzc0p2bHJaTmkzNE1iaFZVQ2o2VlVZcTR3cQ=='}

#instructional_levels = ["beginner","intermediate","expert"]
#categories =["Business", "Design", "Development", "Finance & Accounting", "Health & Fitness", "IT & Software", "Lifestyle", "Marketing", "Music" ,"Office", "Productivity", "Personal Development", "Photography & Video", "Teaching & Academics", "Udemy Free Resource Center", "Vodafone"]
#durations = {"short":"1-3 Hours","medium":"3-6 Hours","long":"6-17 Hours","extralong":"17+ Hours"}

instructional_levels = ["beginner"]
categories =["Business"]
durations = {"short":"1-3 Hours"}

def udemy_run(config, page, store_in_database=True):
    # scrape
    headers = ["name", "provider", "level", "instructor", "description", "duration", "price", "link", "category"]
    courselist = pd.DataFrame(columns=headers)
    
    udemy_url = 'https://www.udemy.com/api-2.0/courses/?page=' + str(page) + '&page_size=100'


    for instructional_level in instructional_levels:
        for category in categories:
            for key, value in durations.items():
                sc = 200
                print('url:', udemy_url)
                args = {
                    "instructional_level" : instructional_level,
                    "duration": key,
                    "language" : "eng",
                    "category" : category,
                    "ratings" : 5
                }

                r = s.get(udemy_url)
                sc = r.status_code
                print('Status Code:', sc)
                if sc != 200:
                    break
                else:
                    print(r.status_code)
                    parsed_response = json.loads(r.text)

                    df = pd.json_normalize(parsed_response['results'])
                    try:
                        df["instructor"] = [d[0].get('title') for d in df.visible_instructors]
                    except:
                        df["instructor"]= "-"

                    try:
                        df["num_reviews"] = [d[0].get('title') for d in df.num_reviews]
                    except:
                        df["num_reviews"]= "-"

                    for index, row in df.iterrows():
                        url = "https://www.udemy.com" + row["url"]
                        instructor =row["instructor"]

                        if str(row["price"]).upper().strip() == 'FREE':
                            row["price"] = '0'
                        else:
                            row["price"] = str(row["price"]).replace('€', '').replace('$', '').replace(',', '').strip()

                        dict = {
                            "name": row["title"],
                            "provider": "Udemy",
                            "level": instructional_level,
                            "instructor": instructor,
                            "description": row["headline"],
                            "duration": value,
                            "price": row["price"],
                            "category" : category,
                            "link": url}

                        print('Data:', dict)

                        courselist = courselist.append(dict, ignore_index=True)

    # courselist
    courselist = labeling_process(courselist)

    if store_in_database == True:
        # add data to database
        for index, row in courselist.iterrows():
            new_item = Smatch_CourseList(row['name'], row['provider'], row['level'], row['instructor'], row['description'], row['duration'], 
                                         row['price'], row['link'], row['category'])
            session.add(new_item)
            session.flush()
            
        try:
            session.commit()
            print('Ok')
        except Exception as e :
            print('error: ', str(e))
            session.rollback()
        finally:
            session.close()
    else:
        # save to csv
        courselist.to_csv('courselist_data.csv')

    config["udemyStatusMessage"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "w") as file:
        file.write(yaml.dump(config))
    
    print('Finished')

### ------------- End Udemy section -----------------

### --------------- UDX section -------------------
### ------------- End UDX section -----------------

### --------------- Coursera section -------------------
### ------------- End Coursera section -----------------


# run
if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = file.read()
    config = yaml.safe_load(config)

    page = 1

    udemy_run(
        config,
        page,
        False
    )