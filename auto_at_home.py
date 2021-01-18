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
import geo_info as gi


def sign():
    log = open('C:/programming/buaa_ncov_auto/sign_at_home.log', 'a')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

    chrome_options = Options()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    chrome_options.add_argument('--headless')
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
        browser.save_screenshot('loaded.png')

    sleep(1)

    # Check if already signed.
    if EC.text_to_be_present_in_element((By.CLASS_NAME, "footers"), "您已提交过信息")(browser) :
        datee = time.asctime()
        print("%s already signed. " % (datee), file=log)
        print("%s already signed. " % (datee))
        log.flush()
        browser.quit()
        log.close()
        return

    # Check if it is too early for sign.
    if EC.text_to_be_present_in_element((By.CLASS_NAME, "footers"), "未到填报时间")(browser) :
        datee = time.asctime()
        print("%s wait for sign, too early. " % (datee), file=log)
        print("%s wait for sign, too early. " % (datee))
        log.flush()
        browser.quit()
        log.close()
        return

    # Load geo info.
    browser.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){" +
                           "var position = {\"coords\" : {\"latitude\": \"" + gi.lz_latitude + "\",\"longitude\": \"" + gi.lz_longitude + "\"}};" +
                           "success(position);}")
    sleep(1)

    # 所在地点
    where = browser.find_element_by_name("area")
    where.click()
    sleep(1)
    browser.save_screenshot('geo.png')

    #今日体温范围
    body_temperature = browser.find_element_by_xpath("//div[@name='tw']/div/div[2]")
    body_temperature.click()
    browser.save_screenshot('tw.png')

    # 是否在校
    not_at_school = browser.find_element_by_xpath("//div[@name='sfzx']/div/div[2]")
    not_at_school.click()
    browser.save_screenshot('sfzx.png')

    #是否请假外出
    ask_for_leave = browser.find_element_by_xpath("//div[@name='askforleave']/div/div[1]")
    ask_for_leave.click()
    browser.save_screenshot('askforleave.png')

    #今日是否返校住宿
    not_return_to_school = browser.find_element_by_xpath("//div[@name='sffxzs']/div/div[2]")
    not_return_to_school.click()
    browser.save_screenshot('sffxzs.png')

    # #是否处于隔离期
    # not_at_quarantine = browser.find_element_by_xpath("//div[@name='sfcyglq']/div/div[2]")
    # not_at_quarantine.click()
    # sleep(0.5)
    # browser.save_screenshot('sfcyglq.png')

    #提交
    footers = browser.find_element_by_class_name('footers')
    footers.click()
    sleep(1)
    browser.save_screenshot('confirm.png')

    #确认
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
