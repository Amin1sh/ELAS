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
        duration_2 = duration_2.split(" ")[0].split("–")[0]
        duration = str((int(duration_1.strip()) * int(duration_2.strip())))
    except:
        duration = "0"
    
    try:
        price = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]").text
        price = price.upper().strip()
        price = '0' if price == 'FREE' else  str(price).replace('€', '').replace('$', '').replace(',', '').strip()
        price = int(price)
    except:
        try:
            price = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]").text
            price = price.upper().strip()
            price = '0' if price == 'FREE' else  str(price).replace('€', '').replace('$', '').replace(',', '').strip()
            # price = int(price)
        except:
            price = "0"
        
        
    dict = {
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
    
    return dict



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
        # try:
        #     browser.execute_script("window.localStorage.clear();")
        #     browser.execute_script("window.sessionStorage.clear();")
        #     browser.execute_script("window.location.reload();")
        # except Exception as e:
        #     print('Error in clear browser cache', str(e))
        #     pass

        #time.sleep(3) # 42 * 3 s
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
            continue

        # scrape list of courses url
        list_of_courses = []
        for i in range(1, 25):
            try:
                xpath = f'//*[@id="main-content"]/div/div[4]/div[2]/div[{str(i)}]/a'
                link = browser.find_element(by=By.XPATH, value=xpath).get_attribute('href')
                list_of_courses.append(link)
            except Exception as e:
                if i == 1:
                    break
        
        browser.close()
                
        for page_url in list_of_courses:
            # s_rnd = random.randint(10, 30)
            # time.sleep(s_rnd) # 42 * 24 * 10-30 s
            try:
                course_info = edx_get_page(page_url)
                data = data.append(course_info, ignore_index=True)
                if store_in_database == False:
                    data.to_csv('edx_before_labeling.csv')
            except Exception as e:
                print(f'Error in scraping url[{page_url}]:', str(e))
                pass

    


    result = labeling_process(data)    

    # result
    # print('result: ', result)

    if store_in_database == True:
        # add data to database (without testing)
        for index, row in data.iterrows():
            new_item = Smatch_CourseList(row['name'], row['provider'], row['level'], row['instructor'], row['description'], row['duration'], 
                                        row['price'], row['link'], row['category'])
            session.add(new_item)
            
        try:
            session.commit()
            print('Ok')
        except Exception as e :
            print('error: ', str(e))
            session.rollback()
        finally:
            session.close()
    else:
        result.to_csv("edx_data.csv")
        
    config["edxStatusMessage"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "w") as file:
        file.write(yaml.dump(config))
### ------------- End EDX section -----------------

### --------------- Coursera section -------------------
coursera_urls = ["https://www.classcentral.com/subject/cs?page="]
coursera_links = []

def coursera_collectlinks(lessons):
    for lesson in lessons:
        name = lesson.find(class_="color-charcoal course-name")
        link = "https://www.classcentral.com" + name.get('href')
        coursera_links.append(link)

def coursera_getclasscenterlink(url):
    print('Downloading page ' + url)

    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    table = soup.find(class_="catalog-grid__results")
    try:
        lessons = table.find_all(class_="bg-white border-all border-gray-light padding-xsmall radius-small margin-bottom-small medium-up-padding-horz-large medium-up-padding-vert-medium course-list-course")
    except:
        return 1

    coursera_collectlinks(lessons)

def coursera_get_details(link,description):
    if link.endswith("classroom"):
        pass
    else:
        res = requests.get(link)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        course = {
            "name": "",
            "instructor": "",
            "description": description,
            "provider": "",
            "level": "",
            "duration": "",
            "price": ""
        }

        #Header
        head = soup.find(class_="bg-white small-down-padding-medium padding-large radius-small border-all border-gray-light cmpt-grid-header margin-bottom-medium")
        course["name"] = head.find(class_="head-1").text
        course["instructor"] = head.find(class_="link-gray-underline text-1").get_text().strip()

        #Things in Flex table
        tables = soup.find(class_="bg-white small-down-padding-medium padding-large border-all border-gray-light radius-small margin-bottom-medium")
        course["link"] = "https://www.classcentral.com" + tables.find(class_="margin-bottom-small btn-blue btn-medium width-100").get('href')
        table = tables.find('ul')
        blob = table.find_all("li")
        for element in blob:

            # Provider
            if element.find(class_="icon-provider-charcoal icon-medium") != None:
                course["provider"] = element.find("a").get_text().strip()

            # Level
            if element.find(class_= "icon-level-charcoal icon-medium") != None:
                course["level"] = element.find(class_="text-2 margin-left-small line-tight").get_text().strip()

            #Duration
            if element.find(class_= "icon-clock-charcoal icon-medium") != None:
                course["duration"] = element.find(class_="text-2 margin-left-small line-tight").get_text().strip()

            #Price
            if element.find(class_= "icon-dollar-charcoal icon-medium") != None:
                course["price"] = element.find(class_="text-2 margin-left-small line-tight").get_text().strip()
        return course

def coursera_getcourselink():
    for urlr in coursera_urls:
        i = 1
        done = 0
        #while done != 1:
        while i != 10:
            url = urlr + str(i)
            done = coursera_getclasscenterlink(url)
            i = i+1

    textfile = open("a_file.txt", "w")
    for element in coursera_links:
        textfile.write(element + "\n")
    textfile.close()


def coursera_run(config, coursera_url, coursera_description, store_in_database=True):
    headers = ["name", "provider", "level", "instructor", "description", "duration", "price", "link"]
    data = pd.DataFrame(columns=headers)
    
    try:
        course = coursera_get_details(coursera_url, coursera_description)
        data = data.append(course, ignore_index=True)
    except:
        pass

    result = labeling_process(data)
    
    # result
    print('result: ', result)

    if store_in_database == True:
        # add data to database (without testing)
        for index, row in data.iterrows():
            new_item = Smatch_CourseList(row['name'], row['provider'], row['level'], row['instructor'], row['description'], row['duration'], 
                                        row['price'], row['link'], row['category'])
            session.add(new_item)
            
        try:
            session.commit()
            print('Ok')
        except Exception as e :
            print('error: ', str(e))
            session.rollback()
        finally:
            session.close()
    else:
        result.to_csv("coursera_data.csv")
        
    config["udemyStatusMessage"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "w") as file:
        file.write(yaml.dump(config))
### ------------- End Coursera section -----------------


# run
if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        config = file.read()
    config = yaml.safe_load(config)

    edx_run(
        config,
        False
    )