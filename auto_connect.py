import sys
import logging
import io
from time import sleep
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import password as pw

def connect():

    chrome_options = Options()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(1080, 1920)

    url = "https://gw.buaa.edu.cn"
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    browser.get(url)
    try :
        login = browser.find_element_by_id("login")
    except NoSuchElementException:
        logged = True
    else:
        logged = False

    if logged:
        logout = browser.find_element_by_id("username")
        logout.click()
        sleep(3)

    username = browser.find_element_by_id("username")
    username.send_keys(pw.net_user)

    password = browser.find_element_by_id("password")
    password.send_keys(pw.net_password)

    login = browser.find_element_by_id("login")

    login.click()
    sleep(10)
    
 