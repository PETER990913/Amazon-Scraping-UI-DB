from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
SCRAPEOPS_API_KEY = 'ab147e77-85aa-4e7f-8be4-6f1b2a685d62'
            
proxy_options = {
    'proxy': {
        'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'no_proxy': 'localhost:127.0.0.1'
    }
}
driver = webdriver.Chrome(seleniumwire_options=proxy_options)        
driver.maximize_window()
driver.get('https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Gymnastics-Leotards/zgbs/')
Firsts = driver.find_elements(By.CSS_SELECTOR, 'div[class="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL"]')
for first in Firsts:
    first_cat = first.text
    print("First_category:", first_cat)
while True:
    pass