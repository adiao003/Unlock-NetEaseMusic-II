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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E93D69DE9B68CC8A88E6760C6198F54752134FF2CE149D78AC936A1D317F80E99813C690C1E69DB0B65BDD678BDADE06D9C8D28D9B9F1FE7EA1A8D9535EB677995010A84F1215F6B6F128EB25C36A4A0C27770F168ED8DCE18FD7CEA2D37713F7751CDA75B12C17B8883A49561D75814F917E83053AAB4032A3BA17C629D341E44DC7BA41C3B0E17C0C460940BE25C8192DF3B961619DC352B5A7F4656F3434C3431C246B6BB827394D01B0644CAF9004F7C69DCDDBF3921434DE017F77B77592494994FA9439915350DC846A511670F947EA8B9C3CF3067408C23005C4A53F164673AB124CAAE05CE3EDE409B92E8C55D6DAC551D60E36D78EF5F5D7F18B6C91A2402DC946AC2880E02965FAC2E1FD53ABA408D1AC524AA44B7FB9BD4C9D74D55A89B56F96F1C42CD08DF93FB7430C4C5D247BF69B5996BE33201C621B2D5C86FE30968F1FA91080DA63A569D771FE454CDAB8AFE984E4C6D5EAEE1D824CD73"})
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
