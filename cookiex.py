
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import InvalidCookieDomainException

import os
import json
import time
import pickle
import undetected_chromedriver as uc



def save_cookie_json(browser, path='cookies'):

    if os.path.exists('cookies'):
        print('cookies exists, rename to cookies.old')

        try:
            os.rename('cookies', 'cookies.old')
        except FileExistsError:
            os.replace("cookies", "cookies.old")

        # Save the cookie as JSON
        with open(path, 'w') as filehandler:
            json.dump(browser.get_cookies(), filehandler)

    else:
        print('cookies does not exist, saving cookies')

        # Save the cookie as JSON
        with open(path, 'w') as filehandler:
            json.dump(browser.get_cookies(), filehandler)



def save_cookie_pickle(browser, path='cookies.pkl'):

    if os.path.exists('cookies.pkl'):
        print('cookies.pkl exists, rename to cookies.pkl.old')

        try:
            os.rename('cookies.pkl', 'cookies.pkl.old')
        except FileExistsError:
            os.replace("cookies.pkl", "cookies.pkl.old")

        # Save the cookie as PICKLE
        pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
        time.sleep(3)

        # !!! DEBUG = Checking if cookies.pkl saved successfully and able to read its contents
        # pickle_cookies = pickle.load(open("cookies.pkl", "rb"))
        # for cookie in pickle_cookies:
        #     print(cookie)

    else:
        print('cookies.pkl does not exist, saving cookies.pkl')

        # Save the cookie as PICKLE
        pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))  



def gmail_login(TARGET_URL,EMAIL,EMAIL_PASSWORD):

    url = TARGET_URL
    GMAIL = EMAIL
    passWord = EMAIL_PASSWORD

    try:
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-plugins-discovery')
        chrome_options.add_argument("--enable-file-cookies")
        browser = uc.Chrome(options=chrome_options)
        WebDriverWait(driver = browser, timeout = 10).until(lambda x: x.execute_script('return document.readyState === "complete"'))
        browser.delete_all_cookies()
        time.sleep(2)

        browser.get(url)
        time.sleep(2)

        email = browser.find_element(By.ID, 'identifierId')
        email.click()
        email.send_keys(GMAIL)
        time.sleep(2)
        
        email.send_keys(Keys.ENTER)
        time.sleep(5)

        get_source = browser.page_source

        wrong_email = 'find your Google Account'

        if wrong_email in get_source:
            print('Could not find your Google Account')
            
            browser.close()
            browser.quit()
            browser.stop_client()
        
        else:
            actions = ActionChains(browser)
            actions.send_keys(passWord + Keys.ENTER)
            actions.perform()
            time.sleep(5)
            
            get_source = browser.page_source

            wrong_password = 'Wrong password'

            if wrong_password in get_source:
                print('Wrong password. Try again or click Forgot password to reset it')

                browser.close()
                browser.quit()
                browser.stop_client()

            else:
                save_cookie_json(browser)
                time.sleep(2)
                save_cookie_pickle(browser)
                time.sleep(2)
                
                print('Login has been successfully completed')
                time.sleep(2)

                browser.close()
                browser.quit()
                browser.stop_client()

    except Exception as e:
        pass

        # !!! DEBUG = Print error message if unable to login
        # print(e)



def load_cookie_pickle(browser, path='cookies.pkl'):

    # Load cookies.pkl and read its contents
    pickle_cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in pickle_cookies:
        try:
            browser.add_cookie(cookie)

            # !!! DEBUG = Check if cookies added successfully
            # print(cookie)
        except InvalidCookieDomainException as e:
            pass

            # !!! DEBUG = Print error message if unable to add cookie
            # print(e.msg)



def load_cookie_json(browser, path='cookies'):

    # Load cookies and read its contents
    with open('cookies', 'r') as cookies_file:
        json_cookies = json.load(cookies_file)

    for cookies_data in json_cookies:
        try:
            browser.add_cookie(cookies_data)

            # !!! DEBUG = Check if cookies added successfully
            # print(cookie)
        except InvalidCookieDomainException as e:
            pass

            # !!! DEBUG = Print error message if unable to add cookie
            # print(e.msg)




def login_with_cookie(TARGET_URL):

    url = TARGET_URL

    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-plugins-discovery')
    chrome_options.add_experimental_option('detach', True)
    chrome_options.add_argument("--enable-file-cookies")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(executable_path=r'Selenium_WebDriver\chromedriver.exe', options=chrome_options)
    WebDriverWait(driver = browser, timeout = 10).until(lambda x: x.execute_script('return document.readyState === "complete"'))
    browser.get('http://www.google.com')
    browser.delete_all_cookies()
    time.sleep(2)

    # Load PICKLE format cookie
    # load_cookie_pickle(browser)
    # time.sleep(2)

    # Load JSON format cookie
    # load_cookie_json(browser)
    # time.sleep(2)

    # Load JSON format cookie of SharpCookieMonster
    load_cookie_json(browser,'Untitled-1.json')
    time.sleep(2)

    # Check if cookies added successfully
    print(browser.get_cookies())
    time.sleep(2)

    browser.get(url)
    time.sleep(2)




if __name__ == "__main__":

    # Provide the targeted Google URL
    TARGET_URL = ''

    # Provide the targeted email address
    EMAIL = ''

    global browser

    if ( (os.path.exists('cookies')) and (os.path.exists('cookies.pkl')) ):
        print('cookies exists, login using cookies')

        login_with_cookie(TARGET_URL)

    else:
        print('cookies and cookies.pkl does not exist, loading login page')

        EMAIL_PASSWORD = getpass('Enter Password:')
        time.sleep(2)
        
        gmail_login(TARGET_URL,EMAIL,EMAIL_PASSWORD)

