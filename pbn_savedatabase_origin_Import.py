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
import json
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
driver.get('https://www.amazon.com/Best-Sellers-Digital-Music/zgbs/dmusic/ref=zg_bs_nav_dmusic_0')
import time
JSON_list = []
new_JSON = {}

def call_back(driver):
    item_tables = driver.find_element(By.CSS_SELECTOR, 'div[role="group"]')
    item_table = item_tables.find_elements(By.CSS_SELECTOR, 'div[role="treeitem"]')
    for i in range(0, len(item_table)):
    # for item in item_table:
        if i != 0:
            item_tables = driver.find_element(By.CSS_SELECTOR, 'div[role="group"]')
            item_table = item_tables.find_elements(By.CSS_SELECTOR, 'div[role="treeitem"]')
        print('ITEM:::', item_table[i])
        print("############### Indexing number: ", i)
        item_text = item_table[i].get_attribute('innerText')
        item_link_initial = item_table[i].find_element(By.TAG_NAME, 'a').get_attribute('href')      
        # print('Item Text:::', item_text)  
        # print('item_link_new:::', item_link_initial)
        driver.get(item_link_initial)       
        time.sleep(5)
        new_item_tables = driver.find_element(By.CSS_SELECTOR, 'div[role="group"]')
        item_link_element = new_item_tables.find_elements(By.TAG_NAME, 'span')
        if (item_link_element):
            print('----------------------------IF---------------------')
            item_link = item_link_initial          
            # print('Item Link:::', item_link)
            json_data = {"name": item_text, "link": item_link}
            print(json_data)
            file = open("DigitalMusic.json", "a")
            json.dump(json_data, file)
            file.write('\n')
            file.close()
            # driver.back()
        else:
            print('---------------------------ELSE---------------------')   
            json_data = {"name": item_text, "link": ""}
            print(json_data)
            file = open("DigitalMusic.json", "a")
            json.dump(json_data, file)
            file.write('\n')
            file.close()
            call_back(driver)
            
        file = open("DigitalMusic.json", "a")
        driver.back()
        file.write("back" + "\n")
        file.close()
        time.sleep(1)

call_back(driver)
print("call ended")

    
while True:
    pass
