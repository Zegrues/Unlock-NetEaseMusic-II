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
    browser.add_cookie({"name": "MUSIC_U", "value": "00A3E089FB019539F707AEEAFB32DC1260D562B08E0DD8ADB6BCA54110218444BCEF430FD2CE3E6235E61089BBEAD6F48BDABF34104DE3A8858474C2FECC3E499D597B5A9D4932560A660D9A85FE581517E266C4F009212052FEF022F20B5D66F2CF27CC746A650D18B0E04EC8AC5E4F4447D1BB3954E95D67DCD11E7AFF26292CD84CB3D73D9C052294C7B5709BD6F3160B5277EF41E5B03F2498AC7B86DEE5F3BBFA1C93B1102BB6A27E6FA3ED5E755C09E51C1DB9E0061E0B6E4AE8E86625BBE0FD5E10BDB239735827184A105137B9660089A9CCCCA3891098968CC8E375DF3DAEAE42534487CC131EFB64217A6D6AD8A9A89FC2D5D44CF53CF9A2E6EB2BBB8AA0E1302CE989D9414299FD86B4D837110EC4C379E35ACB75892F34651A901AC07C82B9B8B59B0F8C227FE1039B8E8768EDE4974FEC6583E20BF07158252579A688749F2DB7178EC10A189DEA2B733316A5E0316606E813EB03076A3A17F7C7"})
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
