from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
SCRAPEOPS_API_KEY = 'ab147e77-85aa-4e7f-8be4-6f1b2a685d62'


def load_treeItems(driver):
    Group = driver.find_element(By.CSS_SELECTOR, 'div[role="group"]')
    span_elements = Group.find_elements(By.TAG_NAME, 'span')
    json_items = []
    if(len(span_elements)):
        print("span")
        return []
    else:
        print("find treeitems")
        tree_items = Group.find_elements(By.CSS_SELECTOR, 'div[role="treeitem"]')
        for tree_item in tree_items:
            json_item = {}
            text = tree_item.text
            print("text:", text)
            initial_link = tree_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
            json_item['text'] = text
            json_item['link'] = initial_link
            tree_item.click()
            json_item['treeitems'] = load_treeItems(driver)
            json_items.append(json_item)
            print("json_itesm: ", json_items)
            #back to the previous link
            driver.back()
        return json_items
        
    
                    
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
load_treeItems(driver)
        

    

while True:
    pass