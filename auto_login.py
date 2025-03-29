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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D039BA874E50E5994133D8A2D73A002AA308BE2D67D9E9D0BDFF797751A7E0BA3FC18EB7F8E6C00887D7A91A1AF89C4548882E760EB053A23A130E6BCA09B9E7ADED735B9DEC6701BED10E214FC5021CBA7B6BE6956871FC7267C14522825248E2A9F86D796D8121269A90CCC2693E3B0AA59F2BA305202EDC4535F53CF8B5A29679835BD67CD4587EC524B8F49A284ABBF9575E8F1FE620044E16B00F8F3D9943351B376203812F1AD53ECB6AA11243B406D4B09EC1C424A3B1B605B707389F70E44239BBC2D2EA331D7454664964FA3287A199EB7CB93648840A21C64993172C2431FBC556DC4A687A7712451D26A0139F55FC346CAD1E29047D3521C5DD79B351E45A3D09F1D09C12DD773BF2818B5FAE7DA9CA82350AA5C434049B3DEA580BBE466C40869D77DC8B02008E6E4AD6828010830B710217F5DF8C989805A8F2E15152C478CE91F244096ED583CBC594"})
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
