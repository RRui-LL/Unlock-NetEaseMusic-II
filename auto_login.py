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
    browser.add_cookie({"name": "MUSIC_U", "value": "00652B3D95340D53E7DDDA34D39FBC52C13F89F80C01FAEE0CC7F5993F9B59673220A8897CC6D814AB0C0057E6DA3DA65BFA45B8980A9358EA60DCA2B0E94EF74207A99601B7402619D5743930EFF6937E19A5E2C3977EDD9F6998E8619943E1B43A3BD3D9CC52F29D862CF28983923532CABD75C2CF97939874B5AE183EAFE778AF2B910B6DD29439EB2D6BE87D7F4FE9396E014C0D303B49591A5302702F4ADD09EE5A0A2B81CE8E329896B152710BF642832D21E12F17FFA3BE2950B7B601CBBEDFD33DA24D652595FB4103AD494B8AC19392DE6E8E3745B7D24E11335147A31DB9C589E01D9F78F421CFF80988A463E182A93B5812AD613156638E8D1947DEA41B0F285B92A5851BC5D4278227ACF136F6444390D71D1B435C82125251673EC4DAAEDDD1944AFA27B6EAAB4C8D09AB4B4A3AA37A1AAB53D4FDADF7E175794951C29311561B4016AB49BE481ACE76F9"})
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
