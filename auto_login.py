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
    browser.add_cookie({"name": "MUSIC_U", "value": "003C22638DF36B2CC2D5A8B74EE925850DF3D7C417C3E41CE8CC9C02F8993FC73421FC7F838A244FDE16C8F465391D544E457567D42E9FBE8AA0F8FFF75CCFA5AA27527C07CA4FEEE49C77F9D204B199F02A8802BBC67BA07CAFA4A555DDE255EE0A0BEFE77C434563F75D8BE3F44D07E2605DB6A1E098B8D607BD0DB4551AE6B62E5707F016F2AB9ADEE5DCB675963EFB38630CAE0DFCF63F2DCB539036A5F15C3C28197A51D16738B821AA882B3364623731C045B970F6193BD6012D14CBA258B752C524301878EADAED807BA513138EB727BE4873B5D208F97CFDB15253BCCE341310A498B6A2CC33714A1C0EACE079828334F33FE6D5B9C64623923D5F4DAC7F301E91AFCBA44542659572129AD9D72C761E386478602709EC56CB7F88CA237DC411ADD31C3998C168D3E33D8A4E8E6FD041E115246DE9FBC08BBF83734F7435CE893891961BDAE2026F023AE06D943A833CE8F5E088C0C03DDCC60665E9CC9D135802005064A5E414548F4222B60A796855C45E32FAD88E3A31E76F9C844D1FC7739D0FC39D124DA8F2DB0A864CED"})
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
