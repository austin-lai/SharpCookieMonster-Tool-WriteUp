#!/usr/bin/env python3

#================================================================
# HEADER
#================================================================
#- IMPLEMENTATION
#-    title           cookiex.py v0.0.2
#-    version         cookiex.py v0.0.2
#-    author          Austin Lai
#-    date            31/10/2022
#-    notes           Note for the script
#-
#================================================================
#  HISTORY
#     21/10/2022 : Austin Lai : Script creation
#     31/10/2022 : Austin Lai : Add options and improvements
# 
#================================================================
#
#   #############################################################
#   # Script can be modified to statically specify email address and URL
#   # It can be a list form as well
#   # Statically specify targeted URL here.
#   # TARGET_URL = ''
#   # Statically specify targeted email address here.
#   # EMAIL = ''
#   ##############################################################
#
#% usage: cookiex.py function[extract|import] EMAIL URL [options]
#%
#%  'cookiex.py' is a tool to automate the process of cookies extraction AND/OR import cookies to Chromium. 
#%  'Password' will be prompted for you to key in.
#%
#% positional arguments:
#%   {extract,import}  
#%                     extract:
#%                     Use 'cookiex.py' to extract cookies.
#%                     Provide email address + password along with target URL.
#%
#%                     import:
#%                     Use 'cookiex.py' to import cookies.
#%                     Provide email address + password along with target URL.
#%                     When using 'import' mode, you will need Selenium WebDriver (chromedriver.exe).
#%                     - You can download from 'https://chromedriver.chromium.org/downloads'.
#%                     - You may need corresponding version of 'chromedriver'.
#%
#%                     - If you not using 'cookiex.py' to extract cookies,
#%                       you will need to save the cookies in JSON format;
#%                       with the filename as 'cookies.json';
#%                       and put it in the same directory as the script.
#%
#%   EMAIL             Specify target email.
#%
#%   URL               Specify target url to be used with the cookies.
#%
#% options:
#%   -h, --help        show this help message and exit
#%
#% EXAMPLES
#%    python3 cookiex.py extract xxx@xxx.xxx https://xxx.xxx.xxx
#%    python3 cookiex.py import xxx@xxx.xxx https://xxx.xxx.xxx
#%
#================================================================
#  TODO
#    
#
#================================================================
# END_OF_HEADER
#================================================================

from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import InvalidCookieDomainException

import re
import os
import sys
import json
import time
import pickle
import textwrap
import argparse
import undetected_chromedriver as uc



def save_cookie_json(browser, path = 'cookies.json'):

    if os.path.exists('cookies.json'):
        print('\'cookies.json\' exists, rename to cookies.json.old')

        try:
            os.rename('cookies.json', 'cookies.json.old')
        except FileExistsError:
            os.replace('cookies.json', 'cookies.json.old')

        # Save the new cookie as JSON file with the filename 'cookies.json'
        with open(path, 'w') as filehandler:
            json.dump(browser.get_cookies(), filehandler)

    else:
        print('\'cookies.json\' does not exist, saving \'cookies.json\'')

        # Save the new cookie as JSON format with the filename 'cookies.json'
        with open(path, 'w') as filehandler:
            json.dump(browser.get_cookies(), filehandler)



def save_cookie_pickle(browser, path = 'cookies.pkl'):

    if os.path.exists('cookies.pkl'):
        print('\'cookies.pkl\' exists, rename to \'cookies.pkl.old\'')

        try:
            os.rename('cookies.pkl', 'cookies.pkl.old')
        except FileExistsError:
            os.replace('cookies.pkl', 'cookies.pkl.old')

        # Save the new cookie as PICKLE format with the filename 'cookies.pkl'
        pickle.dump( browser.get_cookies() , open('cookies.pkl','wb'))
        time.sleep(3)

        # !!! DEBUG = Checking if cookies.pkl saved successfully and able to read its contents
        # pickle_cookies = pickle.load(open('cookies.pkl', 'rb'))
        # for cookie in pickle_cookies:
        #     print(cookie)

    else:
        print('\'cookies.pkl\' does not exist, saving \'cookies.pkl\'')

        # Save the cookie as PICKLE
        pickle.dump( browser.get_cookies() , open('cookies.pkl','wb'))  



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
        chrome_options.add_argument('--enable-file-cookies')
        browser = uc.Chrome(options = chrome_options)
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



def load_cookie_pickle(browser, path = 'cookies.pkl'):

    # Load cookies.pkl and read its contents
    pickle_cookies = pickle.load(open('cookies.pkl', 'rb'))
    for cookie in pickle_cookies:
        try:
            browser.add_cookie(cookie)

            # !!! DEBUG = Check if cookies added successfully
            # print(cookie)
        except InvalidCookieDomainException as e:
            pass

            # !!! DEBUG = Print error message if unable to add cookie
            # print(e.msg)



def load_cookie_json(browser, path = 'cookies.json'):

    # Load cookies and read its contents
    with open('cookies.json', 'r') as cookies_file:
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
    chrome_options.add_argument('--enable-file-cookies')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(executable_path = r'Selenium_WebDriver\chromedriver.exe', options = chrome_options)
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
    load_cookie_json(browser,'cookies.json')
    time.sleep(2)

    # Check if cookies added successfully
    print(browser.get_cookies())
    time.sleep(2)

    browser.get(url)
    time.sleep(2)



RE_EMAIL = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
def email_type(value):
    if not RE_EMAIL.match(value):
        raise argparse.ArgumentTypeError(value + ' is not a valid email address format')
    return value



if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                    prog = os.path.basename(sys.argv[0]),
                    description = ' \'%(prog)s\' is a tool to automate the process of cookies extraction AND/OR import cookies to Chromium. \n \'Password\' will be prompted for you to key in.\n',
                    usage = '%(prog)s function[extract|import] EMAIL URL [options]',
                    epilog = '',
                    add_help = True,
                    prefix_chars = '-/',
                    formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument('function',
                        type = str,
                        choices = ['extract','import'],
                        help = textwrap.dedent('''
                        extract:
                        Use \'%(prog)s\' to extract cookies.
                        Provide email address + password along with target URL.
                        
                        import:
                        Use \'%(prog)s\' to import cookies.
                        Provide email address + password along with target URL.
                        When using \'import\' mode, you will need Selenium WebDriver (chromedriver.exe).
                        - You can download from \'https://chromedriver.chromium.org/downloads\'.
                        - You may need corresponding version of \'chromedriver\'.\n
                        - If you not using \'cookiex.py\' to extract cookies,
                          you will need to save the cookies in JSON format;
                          with the filename as \'cookies.json\';
                          and put it in the same directory as the script.\n
                        '''))

    parser.add_argument('EMAIL',
                        type = email_type,
                        help = textwrap.dedent('''\
                        Specify target email.\n
                        '''))

    parser.add_argument('URL',
                        type = str,
                        help = textwrap.dedent('''\
                        Specify target url to be used with the cookies.
                        '''))

    parser.parse_args(args = None if sys.argv[1:] else ['--help'])


    ################################################################
    # Script can be modified to statically specify email address and URl
    # It can be a list form as well
    # Statically specify targeted URL here.
    # TARGET_URL = ''
    # Statically specify targeted email address here.
    # EMAIL = ''
    ################################################################


    global browser

    args = parser.parse_args()
    
    if args.function == 'extract':
        print('Using ' + os.path.basename(sys.argv[0]) + ' \'extract\' function.\n')

        EMAIL_PASSWORD = getpass('Enter Password for ' + args.EMAIL + ':')
        time.sleep(2)
        
        gmail_login(args.URL,args.EMAIL,EMAIL_PASSWORD)

    elif args.function == 'import':
        print('Using ' + os.path.basename(sys.argv[0]) + ' \'import\' function.\n')

        if ( (os.path.exists('cookies.json')) and (os.path.exists('cookies.pkl')) ):
            print('\'cookies.json\' and \'cookies.pkl\' exists, using extracted cookies to login.')

            login_with_cookie(args.URL)

        else:
            print('\'cookies.json\' and \'cookies.pkl\' do not exist.\n')
            print('You need to extract cookies using SharpCookieMonster.')
            print('OR')
            print('Use ' + os.path.basename(sys.argv[0]) + ' \'extract\' function to extract the cookies if you have the password.\n')

    else:
        parser.parse_args('--help')

