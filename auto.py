import sys
import io
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import time

import password as pw

longitude = "103.70565"                  # 定位经度
latitude = "36.087104"                   # 定位纬度

def sign():
    log = open('./rua.log', 'a')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

    chrome_options = Options()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(720, 1280)

    url = "https://app.buaa.edu.cn/site/ncov/xisudailyup"
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    browser.get(url)

    try:
        user = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.TAG_NAME, "input")))
    finally:
        sleep(1)
        browser.save_screenshot('login.png')

    username = browser.find_element_by_tag_name('input')
    username.send_keys(pw.uni_user)

    password = browser.find_element_by_xpath("//input[@type='password']")
    password.send_keys(pw.uni_password)

    login_button = browser.find_element_by_css_selector('div.btn')

    browser.execute_script("$(arguments[0]).click()", login_button)

    try:
        element = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[@name='sfzx']/div/div[1]")))
    finally:
        browser.save_screenshot('load.png')

    sleep(1)

    if EC.text_to_be_present_in_element((By.CLASS_NAME, "footers"), "您已提交过信息")(browser) :
        datee = time.asctime()
        print("%s already signed. " % (datee), file=log)
        log.flush()
        browser.quit()
        log.close()
        return

    if EC.text_to_be_present_in_element((By.CLASS_NAME, "footers"), "未到填报时间")(browser) :
        datee = time.asctime()
        print("%s wait for sign, too early. " % (datee), file=log)
        log.flush()
        browser.quit()
        log.close()
        return
    sleep(1)

    browser.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){" +
                           "var position = {\"coords\" : {\"latitude\": \"" + latitude + "\",\"longitude\": \"" + longitude + "\"}};" +
                           "success(position);}")

    sleep(1)

    where = browser.find_element_by_name("area")
    where.click()
    sleep(3)

    not_at_school = browser.find_element_by_xpath("//div[@name='sfzx']/div/div[2]")
    not_at_school.click()
    sleep(1)

    temperature = browser.find_element_by_xpath("//div[@name='tw']/div/div[2]")
    temperature.click()
    sleep(1)

    browser.save_screenshot('geo.png')

    footers = browser.find_element_by_class_name('footers')
    footers.click()
    sleep(1)

    browser.save_screenshot('confirm.png')

    confirm = browser.find_element_by_class_name('wapcf-btn-ok')
    confirm.click()
    sleep(1)

    browser.save_screenshot('signed.png')
    datee = time.asctime()

    print("%s signed successfully! " % (datee), file=log)
    print("%s signed successfully! " % (datee))
    log.flush()

    browser.quit()
    log.close()


def main(): 
  
    sign()


main()
