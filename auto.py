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

import auto_connect

import password as pw

longitude = "116.34519775126265"                  # 定位经度
latitude = "39.982642289294574"                   # 定位纬度

def sign():
    log = open('./rua.log', 'a')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

    chrome_options = Options()
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(1080, 1920)

    url = "https://app.buaa.edu.cn/site/ncov/xisudailyup"
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    browser.get(url)

    try:
        user = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.TAG_NAME, "input")))
    finally:
        browser.save_screenshot('picture1.png')

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
        browser.save_screenshot('picture1.png')

    if EC.text_to_be_present_in_element((By.CLASS_NAME, "footers"), "您已提交过信息") :
        datee = datetime.date.today()
        print("%s already signed " % (datee), file=log)
        log.flush()
        browser.quit()
        log.close()
        quit()

    browser.execute_script("window.navigator.geolocation.getCurrentPosition=function(success){" +
                           "var position = {\"coords\" : {\"latitude\": \"" + latitude + "\",\"longitude\": \"" + longitude + "\"}};" +
                           "success(position);}")

    at_school = browser.find_element_by_xpath("//div[@name='sfzx']/div/div[1]")
    at_school.click()

    temperature = browser.find_element_by_xpath("//div[@name='tw']/div/div[2]")
    temperature.click()

    where = browser.find_element_by_name("area")
    where.click()

    browser.save_screenshot('geo.png')

    footers = browser.find_element_by_class_name('footers')
    footers.click()

    browser.save_screenshot('confirm.png')

    confirm = browser.find_element_by_class_name('wapcf-btn-ok')
    confirm.click()

    browser.save_screenshot('ok.png')
    datee = datetime.date.today()

    print("%s signed successfully! " % (datee), file=log)
    print("%s signed successfully! " % (datee))
    log.flush()

    browser.quit()
    log.close()


def main():  # 0:05进行打卡
  
    sign()


main()
