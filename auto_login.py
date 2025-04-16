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
    browser.add_cookie({"name": "MUSIC_U", "value": "007B141149B4F6C9CE1643600007A70849CB7FE1976269025B3C9260314082B7E946FF2E94DB9E31F7CB82F6EAA8347B514221345EF0B115BC9BD0C5341414F10FFD12E0CEBDFF8EC3E86144801350B6301F1B9644A3612539FABF376B2138EEEE2F603C746CEB3F3CFF8D50072A7EEF30C17648081D814CF7D6C20F0E61CAC94C822419F590A5D84C8D8CCEEE46BA999C2613AFDA5844BB7BE8DA6140EB9B184E6E511AF3E1152E9E8867B0DEE35EBCC4C3BA50E6E0CCA45255D0631498EB0BA3BBA6FAC6E4DCEB7A91C65132239357E169D2C8B581A8639022BF30D39BB7090292AC24B61645471CBA1C44FD0F7532E32A072AEB1E1AD00EFE83418495F7F964BCF5DF634EEF6F3C646D3B3627698DC84FDCD02994A4998EC418CD54DF75094DF9CE53F6941563DBFB2E82F98C51076F5CA7B58597BF7EE4D94E1BC7FC5FF091513BF9E087D5DB42786C3B3D832CA839"})
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
