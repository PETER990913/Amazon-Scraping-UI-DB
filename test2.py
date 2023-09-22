from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
import time
import re

SCRAPEOPS_API_KEY = '8e34199a-c66a-4d97-ab7d-2d0b48764a87'

proxy_options = {
    'proxy': {
        'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'no_proxy': 'localhost:127.0.0.1'
    }
}

#
# Product_title_list = []
# Product_image_URL_list = []
# Product_brand_list = []
# Product_Rate_list = []
# Product_Rating_list = []
# Product_price_list = []
# Product_tables_class_name = 'zg-grid-general-faceout'
# Product_image_URL_XPATH = '//*[@id="landingImage"]'
# Product_brand_XPATH = '//*[@id="bylineInfo"]'
# Product_Rate_XPATH = '//*[@id="acrPopover"]/span[1]/a/span'
# Product_Rating_XPATH = '//*[@id="acrCustomerReviewText"]'
# Product_price_Class1 = '_cDEzb_p13n-sc-price_3mJ9Z'
# Product_price_Class2 = 'p13n-sc-price'
# Next_page_XPATH = '//*[@id="CardInstanceVCC9iK3UsqjMrhI_ELT2fA"]/div[2]/div[2]/ul/li[4]'
# # print("link", item_link[0])
# options = webdriver.ChromeOptions()
# options.add_argument('--proxy-server=http://proxy.scrapeops.io:5353')
# options.add_argument('--disable-extensions')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')

# print('--------------------Automation scraping is successfully started-------------------')

## Set Up Selenium Chrome driver
driver = webdriver.Chrome(
    # ChromeDriverManager().install(),
    seleniumwire_options=proxy_options,
    # seleniumwire_options=proxy_options
    )

# driver.maximize_window()
URL = "https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices/ref=zg_bs_nav_amazon-devices_0"
# URL = "https://pypi.org/project/webdriver-manager/"
driver.get(URL)
time.sleep(10)
html_response = driver.page_source
# Saving as EXCEL file
print('fetching done...')
print(html_response)
print('---------------------------Saving result as an Excel--------------------------------')
