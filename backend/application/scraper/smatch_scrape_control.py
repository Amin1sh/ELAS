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

import json, requests, bs4
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import random

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


### --------------- EDX section -------------------
def edx_get_page(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    
    browser.get(url)
    name = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[1]/div[1]/div[5]/div[1]/h1").text
    provider = "edx"
    
    try:
        level_1 = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[3]").text
        level = level_1.partition(": ")[2]
    except:
        level = "-"
        
    
    try:
        subject = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[2]").text
        subject = subject.partition(": ")[2]
    except:
        subject = "-"
    
    
    try:
        instructor = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[1]/a").text
    except:
        instructor = "-"
    
    
    try:
        description = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[4]/div[1]/div[1]/div[2]/div[1]").text
    except:
        description = "-"
    
    
    try:
        duration_1 = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]").text
        duration_1 = duration_1.split(" ")[0]
        duration_2 = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]").text
        duration_2 = (duration_2.split(" ")[0]).split("–")[0]
        duration = str((int(duration_1.strip()) * int(duration_2.strip())))
    except:
        duration = "0"
    
    try:
        price = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]").text
        price = price.upper().strip()
        price = '0' if price == 'FREE' else str(price).replace('€', '').replace('$', '').replace(',', '').strip()
        price = price.strip().split(' ')[0]
        price = int(price)
    except:
        try:
            price = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]").text
            price = price.upper().strip()
            price = '0' if price == 'FREE' else str(price).replace('€', '').replace('$', '').replace(',', '').strip()
            price = price.strip().split(' ')[0]
            price = int(price)
        except:
            price = "0"
        
        
    course_info = {
        "name":name,
        "provider":provider,
        "level": level,
        "instructor": instructor,
        "description": description,
        "duration": duration,
        "price": price,
        "link": url,
        "category": subject
    }
    
    browser.close()
    
    return course_info

def edx_run(config, store_in_database=True):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(options=chrome_options)

    headers = ["name", "provider", "level", "instructor", "description", "duration", "price", "link", "category"]
    data = pd.DataFrame(columns=headers)

    print('Start edx scraping...')
    browser.get(f'https://www.edx.org/search?tab=course')
    time.sleep(5)
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
    
    # find the number of pages
    try:
        xpath = "//ul[contains(@class, 'pagination')]/li[6]/button"
        last_page_number = browser.find_element(by=By.XPATH, value=xpath).text
        last_page_number = int(str(last_page_number).strip())
        print('Last page number:', last_page_number)
    except:
        print("Can't found last page number")
        last_page_number = 42

    browser.close()

    # last_page_number = 1
        
    for page_number in range(1, (last_page_number + 1)):
        browser = webdriver.Chrome(options=chrome_options)

        print('Page:', page_number)

        retries = 3
        while retries > 0:
            try:
                browser.get(f'https://www.edx.org/search?tab=course&page={str(page_number)}')
                time.sleep(5)
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(3)
                break
            except Exception as e:
                print('Try Error:', str(e))
                retries = retries - 1
                pass

        if retries == 0:
            print("Didn't scrape page:", page_number)
            continue

        # scrape list of courses url
        list_of_courses = []
        for i in range(1, 25):
            try:
                xpath = f'//*[@id="main-content"]/div/div[4]/div[2]/div[{str(i)}]/a'
                xpath = '//*[@id="main-content"]/div/div[4]/div[2]/div[' + str(i) + ']/a'
                link = browser.find_element(by=By.XPATH, value=xpath).get_attribute('href')
                list_of_courses.append(link)
            except Exception as e:
                if i == 1:
                    break
        
        browser.close()
                
        for page_url in list_of_courses:
            try:
                course_info = edx_get_page(page_url)
                data = data.append(course_info, ignore_index=True)
            except Exception as e:
                print(f'Error in scraping url[{page_url}]:', str(e))
                pass

    


    result = labeling_process(data)

    # result
    # print('result: ', result)

    if store_in_database == True:
        # add data to database (without testing)
        for index, row in result.iterrows():
            check_exists = session.query(Smatch_CourseList).filter(Smatch_CourseList.link == row['link']).first()
            
            if check_exists is None:
                # insert
                new_item = Smatch_CourseList(row['name'], row['provider'], row['level'], row['instructor'], row['description'], row['duration'], 
                                        row['price'], row['link'], row['category'])
                session.add(new_item)
            else:
                # update
                check_exists.provider = row['provider']
                check_exists.level = row['level']
                check_exists.instructor = row['instructor']
                check_exists.description = row['description']
                check_exists.duration = row['duration']
                check_exists.price = row['price']
                check_exists.category = row['category']
            
            session.flush()

        try:
            session.commit()
            print('Scrape is Done')
        except Exception as e :
            print('error: ', str(e))
            session.rollback()
        
        session.close()
    else:
        result.to_csv("edx_data.csv")
        
    config["edxStatusMessage"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "w") as file:
        file.write(yaml.dump(config))
### ------------- End EDX section -----------------

### --------------- Coursera section -------------------
def coursera_run(config, store_in_database = True):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=2560,1440")
    browser = webdriver.Chrome(options=chrome_options)

    print('start coursera scraping')

    # set custom filter
    browser.get('https://www.coursera.org/courses')
    time.sleep(20)
    try:
        btn_accept = browser.find_element(by=By.XPATH, value="//*[@id='onetrust-accept-btn-handler']")
        btn_accept.click()
        time.sleep(10)
    except:
        pass

    btn_only_course = browser.find_element(by=By.XPATH, value='//main/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/div[2]/label[1]')
    btn_only_course.click()
    time.sleep(2)
    btn_more_lang = browser.find_element(by=By.XPATH, value='//main/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[7]/div[2]/button')
    btn_more_lang.click()
    time.sleep(3)
    btn_select_english = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'cds-Dialog-dialog')]/div[2]/div[2]/div/div[14]/label")
    btn_select_english.click()
    time.sleep(3)
    btn_apply_lang = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'cds-Dialog-dialog')]/div[2]/div[3]/button[1]")
    btn_apply_lang.click()
    time.sleep(3)


    list_courses = []

    page_counter = 0
    while True:
        page_counter += 1
        print('Scraping page:', page_counter)
        time.sleep(3)
        for i in range(1, 13): # 1..12
            try:
                link = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[{str(i)}]/div/div/a").get_attribute('href')
                
                try:
                    title = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[{str(i)}]/div/div/a/div/div[2]/div/h2").text
                except:
                    try:
                        title = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[{str(i)}]/div/div/a/div/div[3]/div/h2").text
                    except:
                        title = '-'
                
                try:
                    level = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[{str(i)}]/div/div/a/div/div[2]/div[2]/p").text
                    level = level.split(' ')[0]
                except:
                    try:
                        level = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[{str(i)}]/div/div/a/div/div[3]/div[2]/p").text
                        level = level.split(' ')[0]
                    except:
                        level = '-'
                
                new_item = {'name': title, 'level': level, 'link': link}
                list_courses.append(new_item)
            except:
                pass
        
        try:
            next_page_elm = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/button[7]")
            is_next_page_elm_disabled = next_page_elm.get_attribute('disabled') is not None # True, False
            
            if is_next_page_elm_disabled:
                break # while True
            else:
                next_page_elm.click()
                time.sleep(3)
        except:
            break


    browser.close()

    # list_courses
    # courses page scrape
    list_courses_info = []

    for course_item in list_courses:
        course_info = {
            'name': course_item['name'],
            'provider': 'Coursera',
            'level': course_item['level'],
            'instructor': '-',
            'description': '-',
            'duration': 0,
            'price': 0,
            'link': course_item['link'],
            'category': '-'
        }
        
        retries = 3
        while retries > 0:
            try:
                browser = webdriver.Chrome(options=chrome_options)
                course_page = browser.get(course_item['link'])
                time.sleep(3)
                
                try:
                    course_info['instructor'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[1]/div[1]/div[1]/div/div/div/div[4]/div/div/div/a/div/div/span").text.strip()
                except:
                    pass
                
                try:
                    course_info['description'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[1]/p[1]").text.strip()
                except:
                    pass
                
                try:
                    course_info['duration'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[2]/div/div/div/div[2]/div/div/div[5]/div[2]/div[1]/span[1]").text.strip()
                    course_info['duration'] = course_info['duration'].split(' ')[1].strip()
                    course_info['duration'] = int(course_info['duration'])
                except:
                    try:
                        course_info['duration'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[2]/div/div/div/div[2]/div/div/div[4]/div[2]/div[1]/span[1]").text.strip()
                        course_info['duration'] = course_info['duration'].split(' ')[1].strip()
                        course_info['duration'] = int(course_info['duration'])
                    except:
                        pass
                
                try:
                    course_info['category'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/a").text.strip()
                except:
                    pass
                
                try:
                    course_info['price'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[1]/div/div/div/div/div/div[5]/div/div/div/div/div/div/form/button/span[1]/div[1]/span[1]").text.strip().lower()
                    if 'free' in course_info['price']:
                        course_info['price'] = 0
                    else:
                        print('Price:', course_info['price'])
                        # todo: get price
                        course_info['price'] = 0
                except Exception as e:
                    try:
                        course_info['price'] = browser.find_element(by=By.XPATH, value=f"//main/section[2]/div[1]/div[1]/div[1]/div[1]/section[1]/div[3]/div[1]/div[1]/form[1]/button[1]/span[1]/div[1]/span[1]").text.strip().lower()
                        if 'free' in course_info['price']:
                            course_info['price'] = 0
                        else:
                            print('Price:', course_info['price'])
                            # todo: get price
                            course_info['price'] = 0
                    except:
                        print('Err3:', course_info['link'], str(e))
                        pass
                
                browser.close()

                list_courses_info.append(course_info)

                print(f'Scrape course ({course_info["name"]}) completed')
                break
            except Exception as e:
                print('It Failed, course:', course_info["link"], str(e))
                retries -= 1


    headers = ["name", "provider", "level", "instructor", "description", "duration", "price", "link", "category"]
    data = pd.DataFrame(list_courses_info, columns=headers)

    result = labeling_process(data)    

    # result
    # print('result: ', result)

    if store_in_database == True:
        # add data to database (without testing)
        for index, row in result.iterrows():
            check_exists = session.query(Smatch_CourseList).filter(Smatch_CourseList.link == row['link']).first()
            
            if check_exists is None:
                # insert
                new_item = Smatch_CourseList(row['name'], row['provider'], row['level'], row['instructor'], row['description'], row['duration'], 
                                        row['price'], row['link'], row['category'])
                session.add(new_item)
            else:
                # update
                check_exists.provider = row['provider']
                check_exists.level = row['level']
                check_exists.instructor = row['instructor']
                check_exists.description = row['description']
                check_exists.duration = row['duration']
                check_exists.price = row['price']
                check_exists.category = row['category']

            session.flush()
            
        try:
            session.commit()
            print('Scrap is over.')
        except Exception as e :
            print('error: ', str(e))
            session.rollback()
        
        session.close()
    else:
        result.to_csv("coursera_data.csv")

    config["courseraStatusMessage"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "w") as file:
        file.write(yaml.dump(config))
### ------------- End Coursera section -----------------


# run
if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = file.read()
    config = yaml.safe_load(config)

    # edx_run(config, False)

    coursera_run(config, False)