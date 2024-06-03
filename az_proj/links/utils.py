import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_link_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--log-level=3")  # Suppress unnecessary logs
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Disable logging
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")

    # Disable CSS and JavaScript
    chrome_options.add_argument("--blink-settings=imagesEnabled=false,cssEnabled=false,javascriptEnabled=false")
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.javascript": 2
    })

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_page_load_timeout(10)  # Set page load timeout

    try:
        driver.get(url)
    except Exception as e:
        driver.quit()
        return f"Error: Page load timed out or failed with exception {e}."

    try:
        wait = WebDriverWait(driver, 10)
        name = wait.until(EC.presence_of_element_located((By.ID, "productTitle"))).text.strip()
    except Exception as e:
        driver.quit()
        return f"Error: Product title not found. Exception: {e}"

    try:
        price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price-whole"))).text
        price = re.sub(r'\D', '', price)
    except Exception as e:
        driver.quit()
        return f"Error: Product price not found. Exception: {e}"

    driver.quit()
    return name, price

# def get_link_data(url):
#     headers = {
#     "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
#     "Accept-Language": "en",
#     }

#     r = requests.get(url, headers=headers)
#     soup = BeautifulSoup(r.text, "lxml")
#     name = soup.select_one(selector="#productTitle").getText().strip()
#     price = soup.select_one(selector=".a-price-whole").getText()
#     price = re.sub(r'\D', '', price)

#     return name, price