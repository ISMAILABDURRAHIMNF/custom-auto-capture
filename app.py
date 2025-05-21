import os
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui

options = Options()
options.add_argument('--allow-running-insecure-content')
options.add_argument('--ignore-certificate-errors')

today = date.today().strftime("%Y%m%d")
if not os.path.isdir(f"./capture-{today}"):
    os.makedirs(f"./capture-{today}")

def capture(url):
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5 if "autoreport" in url else 1.5)
    pyautogui.screenshot(f"./capture-{today}/{url.strip().replace(":", ".")}.png")
    print(f"Success: {url} loaded successfully, website captured.")

with open('websites.txt', 'r') as file:
    urls = file.readlines()



for url in urls:
    print(url)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    
    try:
        driver.maximize_window()
        driver.get(f"https://{url}")
        capture(url)

    except TimeoutException:
        print(f"Failed: {url}  did not load within the timeout period.")

    except WebDriverException:
        print(f"{url} cannot opened by htpps, try to use http protocol")
        try:
            driver.get(f"http://{url}")
            capture(url)
        except WebDriverException:
            print(f"Failed: {url} cannot open correclty, please fix this!")
    driver.quit()