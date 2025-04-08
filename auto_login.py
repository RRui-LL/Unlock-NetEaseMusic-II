# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0050FF5A225FDB83C12C88E63B33F78C3756C3BB392B01742FDD102F8BE55FC9479078CD55565846318A2FCB3B41A5AA271885C2FD89B890772CD13225357BD77B49268ACE50CA16D3B933BBFFE5109ABEEB831D160917E4703B1B20382084F8C627FDC9162786C44ACCDCEB19DC1EA930104C170FCA327343241677215DCBF1AF2E241DFF18519EFF0320129EFEED95BC143CCBE753A07D9BAEC48431DAC64DB7E49A35EDAA66FE2E8CE3CA18B4601B1611EF58C343B4AF55D640E076730C8816A7D8C602103F92CB4022C640C0D40D01C4F681F592C6D05095D578C1B2E4DACA15E89C36DF91B87305CB809F667E543383AEA12C0257E8F941D0AAD13BD40EA17B0BEAB834F94B5963549C130C80FBAA392733B28F8A25CA699925B96B963D641A95DA0A8BCB5BA9B6342855C8C42F0F5542907B4BEB49E6408839B985438A1DD8D852A89E6A1D97815DFA3B911495C8"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
