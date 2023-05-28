import json
import pandas as pd
import os
import yaml
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# for add in database
from orm_interface.base import Session
from orm_interface.entities.smatch.smatch_courselist import Smatch_CourseList
session = Session()

### --------------- EDX section -------------------
def edx_get_page(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    
    browser.get(url)
    name = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[1]/div[1]/div[5]/div[1]/h1").text
    provider = "edX"
    
    try:
        level_1 = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[3]").text
        level = level_1.partition(": ")[2]
    except:
        try:
            level_1 = browser.find_element(by=By.XPATH, value="//ul[contains(@class, 'mb-0 pl-3 ml-1')][1]/li[3]").text
        except:
            level = "-"
    
    level = 'Beginner' if level == 'Introductory' else level
        
    
    try:
        subject = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[2]").text
        subject = subject.partition(": ")[2]
    except:
        try:
            subject = browser.find_element(by=By.XPATH, value="//ul[contains(@class, 'mb-0 pl-3 ml-1')][1]/li[2]").text
            subject = subject.partition(": ")[2]
        except:
            subject = '-'
    
    
    try:
        instructor = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[4]/div[1]/div[2]/div[1]/div[1]/div[1]/ul/li[1]/a").text
    except:
        try:
            level_1 = browser.find_element(by=By.XPATH, value="//ul[contains(@class, 'mb-0 pl-3 ml-1')][1]/li[1]/a").text
        except:
            instructor = "-"
    
    
    try:
        description = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'course-about') and contains(@class, 'desktop')]/div[4]/div[1]/div[1]/div[2]/div[1]").text
    except:
        try:
            description = browser.find_element(by=By.XPATH, value="//div[contains(@class, 'preview-expand-component')]/div[2]/div[1]/p[1]/span[1]").text
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
    browser.get(f'https://www.edx.org/search?tab=course&language=English')
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

    if store_in_database == True:
        # add data to database (without testing)
        for index, row in data.iterrows():
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
        data.to_csv("edx_data.csv")
        
    config["edxStatusMessage"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "w") as file:
        file.write(yaml.dump(config))
### ------------- End EDX section -----------------



### --------------- Coursera section -------------------
def coursera_run(config, store_in_database = True):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=2560,1440")
    
    # Set proxy with SOCKS5
    # chrome_options.add_argument("--proxy-server=socks5://localhost:9999")
    
    browser = webdriver.Chrome(options=chrome_options)

    print('start coursera scraping')


    ### new edition
    browser.get('https://www.coursera.org/?authMode=login')
    username_input = browser.find_element(by=By.ID, value='email')
    username_input.send_keys('volid86475@aicogz.com')

    password_input = browser.find_element(by=By.ID, value='password')
    password_input.send_keys('Abc@123456')

    login_button = browser.find_element(by=By.XPATH, value="//button[@type='submit']")
    login_button.click()

    # wait for the manual completion of reCAPTCHA
    time.sleep(30)
    ### end new edition

    # set custom filter
    browser.get('https://www.coursera.org/courses')
    time.sleep(10)
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
                try:
                    link = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[{str(i)}]/div/div/a").get_attribute('href')
                except:
                    try:
                        link = browser.find_element(by=By.XPATH, value=f"(//div[contains(@class, 'css-1j8ushu')])[{str(i)}]//a").get_attribute('href')
                    except:
                        try:
                            link = browser.find_element(by=By.XPATH, value=f"((//ul[contains(@class, 'ais-InfiniteHits-list')])[1]/li[{str(i)}])//a").get_attribute('href')
                        except:
                            print("Can't find course link")
                
                try:
                    title = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[{str(i)}]/div/div/a/div/div[2]/div/h2").text
                except:
                    try:
                        title = browser.find_element(by=By.XPATH, value=f"//main/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/ul/li[{str(i)}]/div/div/a/div/div[3]/div/h2").text
                    except:
                        try:
                            title = browser.find_element(by=By.XPATH, value=f"(//h2[contains(@class, 'css-bku0rr')])[{str(i)}]").text
                        except:
                            try:
                                title = browser.find_element(by=By.XPATH, value=f"(//div[contains(@class, 'css-1j8ushu')])[{str(i)}]//h2").text
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
                        try:
                            level = browser.find_element(by=By.XPATH, value=f"(((//div[contains(@class, 'css-1j8ushu')])[{str(i)}]//p[contains(@class, 'css-14d8ngk')])[last()]").text
                            level = level.split(' ')[0]
                        except:
                            level = '-'
                
                level = 'Advanced' if level == 'Mixed' else level
                
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
        
        
    # json_string = json.dumps(list_courses)
    # with open("output_list_courses.json", "w") as file:
    #     file.write(json_string)
    
    
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
                course_page = browser.get(course_item['link'])
                time.sleep(3)
                
                try:
                    course_info['instructor'] = browser.find_element(by=By.XPATH, value=f"(((//div[contains(@class, 'rc-BannerInstructorInfo')])[1]//a)[1]//span)[1]").text.strip()
                except:
                    try:
                        course_info['instructor'] = browser.find_element(by=By.XPATH, value=f"((//a[@data-track-component='nav_item_instructors'])[1]//text())[1]").text.strip()
                    except:
                        try:
                            course_info['instructor'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[1]/div[1]/div[1]/div/div/div/div[4]/div/div/div/a/div/div/span").text.strip()
                        except:
                            try:
                                course_info['instructor'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[1]/div[1]/div[1]/div/div/div/div[4]/div/div/div/a/div/div/span").text.strip()
                            except:
                                try:
                                    course_info['instructor'] = browser.find_element(by=By.XPATH, value=f"//div[contains(@class, 'instructor-wrapper')][1]//h3[contains(@class, 'instructor-name')]/text()").text.strip()
                                except:
                                    pass
                
                try:
                    course_info['description'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[1]").text.strip()
                except:
                    try:
                        course_info['description'] = browser.find_element(by=By.XPATH, value=f"(//div[contains(@class, 'AboutCourse')][1]//div[contains(@class, 'description')])[1]").text.strip()
                    except:
                        pass
                    
                course_info['description'] = course_info['description'].replace('\'', ' ').replace('"', ' ').replace('\n', ' ').replace('SHOW ALL COURSE OUTLINE', '').replace('SHOW ALL', '').strip()
                
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
                        try:
                            course_info['duration'] = browser.find_element(by=By.XPATH, value=f"(//span[contains(text(), 'Approx') and contains(text(), 'hour')])[2]").text.strip()
                            course_info['duration'] = course_info['duration'].split(' ')[1].strip()
                            course_info['duration'] = int(course_info['duration'])
                        except:
                            pass
                
                try:
                    course_info['category'] = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/a").text.strip()
                except:
                    try:
                        course_info['category'] = browser.find_element(by=By.XPATH, value=f"//div[contains(@role, 'navigation')]/div[2]/a").text.strip()
                    except:
                        try:
                            course_info['category'] = browser.find_element(by=By.XPATH, value=f"(//div[@aria-label='breadcrumbs']//a)[2]").text.strip()
                        except:
                            pass

                course_info['price'] = 0
                bln_enroll_click = False
                try:
                    try:
                        btn_enroll = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[1]/div/div/div/div/div/div[5]/div/div/div/div/div/div/form/button[1]")
                        btn_enroll.click()
                        bln_enroll_click = True
                        time.sleep(5)
                    except:
                        try:
                            btn_enroll = browser.find_element(by=By.XPATH, value=f"//main/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form[1]/button[1]")
                            btn_enroll.click()
                            bln_enroll_click = True
                            time.sleep(5)
                        except:
                            try:
                                btn_enroll = browser.find_element(by=By.XPATH, value=f"//main/section[2]/div[1]/div[1]/div[1]/div[1]/section[1]/div[3]/div[1]/div[1]/form[1]/button[1]")
                                btn_enroll.click()
                                bln_enroll_click = True
                                time.sleep(5)
                            except:
                                try:
                                    btn_enroll = browser.find_element(by=By.XPATH, value=f"(//button[.//span[contains(text(), 'Enroll') and contains(@data-test, 'enroll-button-label')]])[1]")
                                    btn_enroll.click()
                                    bln_enroll_click = True
                                    time.sleep(5)
                                except:
                                    pass  
                    
                    if bln_enroll_click:
                        try:
                            price = browser.find_element(by=By.XPATH, value=f"//div[contains(@class, 'bt3-radio') and contains(@class, 'choice-radio-container')][1]/label/div[2]/div/h4/span[1]/span[3]/span[1]/span").text.strip().lower()
                            price = str(price).replace('€', '').replace('$', '').replace(',', '').strip()
                            course_info['price'] = int(price)
                        except:
                            try:
                                price = browser.find_element(by=By.XPATH, value=f"//span[contains(@class, 'rc-ReactPriceDisplay')]/span[1]").text.strip().lower()
                                price = str(price).replace('€', '').replace('$', '').replace(',', '').strip()
                                course_info['price'] = int(price)
                            except:
                                try:
                                    btn_next = browser.find_element(by=By.XPATH, value=f"//button[contains(@class, 'primary') and contains(text(), 'Next')][1]")
                                    btn_next.click()
                                    time.sleep(5)
                                    
                                    price = browser.find_element(by=By.XPATH, value=f"//span[contains(@class, 'rc-ReactPriceDisplay')]/span[1]").text.strip().lower()
                                    price = str(price).replace('€', '').replace('$', '').replace(',', '').strip()
                                    course_info['price'] = int(price)
                                except:
                                    pass
                    
                except Exception as e:
                    # print('Err3:', course_info['link'], str(e))
                    pass

                list_courses_info.append(course_info)
                
                print(course_info)

                print(f'Scrape course ({course_info["name"]}) completed')
                break
            except Exception as e:
                print('It Failed, course:', course_info["link"], str(e))
                
                ### start new edition
                browser.close()
                
                browser.get('https://www.coursera.org/?authMode=login')
                username_input = browser.find_element(by=By.ID, value='email')
                username_input.send_keys('volid86475@aicogz.com')

                password_input = browser.find_element(by=By.ID, value='password')
                password_input.send_keys('Abc@123456')

                login_button = browser.find_element(by=By.XPATH, value="//button[@type='submit']")
                login_button.click()
                
                # wait for the manual completion of reCAPTCHA
                time.sleep(30)
                ### end new edition

                
                retries -= 1


    browser.close()
    
    headers = ["name", "provider", "level", "instructor", "description", "duration", "price", "link", "category"]
    data = pd.DataFrame(list_courses_info, columns=headers)
    
    # data.to_csv("last_scrape_data.csv")

    if store_in_database == True:
        # add data to database (without testing)
        for index, row in data.iterrows():
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
            print('Ok!')
        except Exception as e :
            print('error: ', str(e))
            session.rollback()
        
        session.close()
    else:
        data.to_csv("coursera_data.csv")

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