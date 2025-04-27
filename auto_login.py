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
    browser.add_cookie({"name": "MUSIC_U", "value": "00DD66A2148F8B87099ED8904ED63ED21CB7E7765BA927ED6D659669EDBF3445DF245EDED6C0E25484DD06753954F2423C7E554790D7C180FBF509BB57AB9D3765E70D35DF216090F1778E5E8BFA236F187F606FA33F83F7B13C852C0C40B9AF3F0CC2EE2D13D4F7B686DE083D61F9BD3B00872F358B123D1A5AC60A32855B3190BF313853929675F54C6908F7A699F747228CDFE0342E676E13850B3BBE27A771C41A790576E61F1902712B3AEE5BB7B46A285941E84C7CDE210610F2B2E34624571D07ACE31FA52B4B3EA56A7E68AE701DAE517A8419A1D996846CCF6715277001443F64643C599F2003F9E07E6ABD8EA3CD9565A1D67B0C5F6FE458D685C44E8DC31820F7ED834D893E156DC3660F6F778E5BD6F2EA8F8EDF730F5614000579996852DF863749ABEB1C686D972B03C48E81BAD5F695D5254D5B5C941D30AEB9D5484FD26EEB4A1658F97BAF92AECE7CC521C21DFCDCF3A56091848620608D7E"})
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
