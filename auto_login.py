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
    browser.add_cookie({"name": "MUSIC_U", "value": "0063E6A3664083858ECBC918BAFF8BECB1FB489F91FCDF9E6B4D043C7D50515E956C61A637E2035DDEE06AAC722781923B3BA9371ACBD8722AD5025BBB7CAB06C0F07C4DA407C22E1623B4B4BF4777FF4D78B4FD8EFCAD32184885799CBDE22AD6D4DA9B2AC7481CFB35AC66A8852050DB3B59D404CC41732BE76FF0A8053CA1FD18C7546A841876143D8733C05B7FE65AFFEE225B2ACA60EE7780F4015A2AD6E6E7A90889330DE3D43D88AD352A7B245714FEF353F8FC67FAF07906D4C138D87D941C35D5C6032A35EC2489A1DC56DE9660948AAFE08A44D29EDF6443CC1D3B8F4ACBC835B55DB67C82D5B732903E92447A563AD9CDD92664F140D2E388419D31036013C08D963DEFEC28C9C9C388491EC30DB220C54AA8D8950A1ABFAE6601DBFC3B5E10153DD9BA38EDE5894C307ECFB4DC4B38151DF042CFFE462EEB5C5FFA90F5F0D896B12834B56371B974DAD2C8"})
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
