# This fixed Daily running and scan depth customizing
from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import re
import logging
from collections import Counter
import datetime

SCRAPEOPS_API_KEY = 'ab147e77-85aa-4e7f-8be4-6f1b2a685d62'
                    
proxy_options = {
    'proxy': {
        'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'no_proxy': 'localhost:127.0.0.1'
    }
}

chrome_options = webdriver.ChromeOptions()
                
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--disable-proxy-certificate-handler')
chrome_options.add_argument('--disable-content-security-policy')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-features=CSSLayoutNG')        

driver = webdriver.Chrome(options=chrome_options,seleniumwire_options=proxy_options)       
driver.maximize_window()

driver.get('https://www.amazon.com/ap/register?showRememberMe=true&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&prevRID=CQ0YWS09K8X97FZ79DSG&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&prepopulatedLoginId=&failedSignInCount=0&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&pageId=usflex&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')

driver.find_element(By.XPATH, '//*[@id="ap_customer_name"]').send_keys('Maurine Runels')
driver.find_element(By.XPATH, '//*[@id="ap_email"]').send_keys('sybylmawyer@gmail.com')
driver.find_element(By.XPATH, '//*[@id="ap_password"]').send_keys('distantclinical0#!')
driver.find_element(By.XPATH, '//*[@id="ap_password_check"]').send_keys('distantclinical0#!')
driver.find_element(By.XPATH, '//*[@id="continue"]').click()



while True:
    pass


seliablacio@gmail.com
spirited#priesthood83#_