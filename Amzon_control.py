# This fixed Daily running and scan depth customizing
from tkinter import Canvas, Entry, Text,  Button, PhotoImage,filedialog,END,Variable,messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
import mysql.connector
import json
import csv
import threading
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
import sys
from PIL import ImageTk, Image

# Save the current sys.stdout for later restoration
original_stdout = sys.stdout

# Specify the file path where you want to save the log
log_file_path = "output.txt"

file_path = "error.txt"

# Open the file in write mode
error_file = open(file_path, "a")

# Connect to the database 
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)

# Check if connection was successful
if mydb.is_connected():
    print("Connected to MySQL database")
# Initializing the global variants

item_text = ""
item_link = ""
Category_result = ""
item_link_list = []
item_text_list = []
category_result_list = []
table_name_list = []
depth_list = []
Product_URL_entry = None
Product_title_entry = None
Product_Price_entry = None
Product_Brand_entry = None
Product_Rating_entry = None
Product_review_entry = None
Product_BSR_entry = None
Product_asin_entry = None
Product_image_URL_entry = None
Product_dimension_entry = None
Product_Date_entry = None
Product_Depth_entry = None
Product_timestamp_entry = None
Product_location_entry = None

# Defining XPATH, CLASSNAME etc...
Product_tables_CSS_SELECTOR = 'div[class="a-cardui _cDEzb_grid-cell_1uMOS expandableGrid p13n-grid-content"]'
Product_image_URL_XPATH = '//*[@id="landingImage"]'
Product_brand_XPATH = '//*[@id="bylineInfo"]'
Product_Rate_XPATH = '//*[@id="acrPopover"]/span[1]/a/span'
Product_Rating_XPATH = '//*[@id="acrCustomerReviewText"]'    
Product_price_Class1 = '_cDEzb_p13n-sc-price_3mJ9Z'
Product_price_Class2 = 'p13n-sc-price'
Product_Month_Sold_XPATH = '//*[@id="social-proofing-faceout-title-tk_bought"]/span'
Product_specification_XPATH = '//*[@id="technicalSpecifications_section_1"]/tbody'
Product_About_Item_XPATH = '//*[@id="feature-bullets"]/ul'
backtoTop_className = 'navFooterBackToTop'

SCRAPEOPS_API_KEY = 'ab147e77-85aa-4e7f-8be4-6f1b2a685d62'
                    
proxy_options = {
    'proxy': {
        'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'no_proxy': 'localhost:127.0.0.1'
    }
}

# defining the Scrape function
def get_all_children(tree, parent_item):
    children = tree.get_children(parent_item)
    all_children = list(children)
    for child in children:
        all_children.extend(get_all_children(tree, child))
    return all_children

def stop_function():
    print("--------------------Scraping is stopped---------------------------")
    global stop_event
    stop_event = threading.Event()
    stop_event.set()
    
def scrape_site():
    global  timestamp, Product_location_entry, Product_URL_entry, Product_Running_entry, Product_title_entry, Product_Price_entry, Product_Brand_entry, Product_Rating_entry, Product_review_entry, Product_BSR_entry, Product_asin_entry, Product_image_URL_entry, Product_dimension_entry, Product_Date_entry, Product_Depth_entry, Product_timestamp_entry, Error_counter_entry
    try:
        with open(log_file_path, "w") as log_file:
            sys.stdout = log_file
            df2 = pd.read_csv("configuration.csv")
            excel_link = df2.Item_link
            category_results_list = df2.Category_result
            table_names_list = df2.table_name
            depth_text_list = df2.Depth
            scan_limit = Product_Depth_entry.get()
            time_interval = Product_Running_entry.get()

            print('scan_limit:::', scan_limit)
            print('time interval:::', time_interval)
            error_number = 0
            while True:
                try:
                    now = datetime.datetime.now()
                    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                    timestamp_text = str(timestamp).replace('-', '').replace(':', '')           
                    # global item_link_list
                    logging.getLogger('webdriver_manager').disabled = True
                    
                    print('--------------------Automation scraping is successfully started-------------------')
                    
                    chrome_options = webdriver.ChromeOptions()
                
                    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
                    chrome_options.add_argument('--disable-proxy-certificate-handler')
                    chrome_options.add_argument('--disable-content-security-policy')
                    chrome_options.add_argument('--ignore-ssl-errors')
                    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
                    chrome_options.add_argument('--disable-features=CSSLayoutNG')        

                    driver = webdriver.Chrome(options=chrome_options,seleniumwire_options=proxy_options)       
                    driver.maximize_window()
                    for link_index in range(0, len(excel_link)):
                        try:
                            # initial result values
                            Product_title_list = []
                            Product_image_URL_list = []
                            Product_brand_list = []
                            Product_Rate_list = []
                            Product_Rating_list = []
                            Product_price_list = []
                            Product_ASIN_list = []
                            Product_Dim_list = []
                            Product_BSR_list = []
                            Product_Month_list = []
                            Product_specification_list = []
                            Product_description_list = []
                            Product_category_list = []
                            Product_Item_list = []
                            Product_Department_list = []
                            Product_Date_list = []
                            Product_Manu_list = []
                            Product_Country_list = []
                            Product_UPSPSC_list = []
                            Product_Special_list = []
                            Product_About_Item_list = []
                            timestamp_list = []
                            Leaf_depth_list = []
                            print("excel_link index: ", link_index)
                            DB_table_name = str(table_names_list[link_index] + timestamp_text).replace(' ', '')
                            print('DB_table_name:::', DB_table_name)
                            URL = excel_link[link_index]
                            print("URL:", URL)
                            Product_location = str(category_results_list[link_index]).replace('Any Department >', '')
                            print("Category:", Product_location)
                            Leaf_Depth = int(depth_text_list[link_index])
                            print('Depth:', Leaf_Depth)
                            Product_category = Product_location
                            Excel_name = str(Product_category + timestamp_text).replace(',', '').replace(' ', '').replace('&', '').replace('-', '').replace('>', '_').replace(':', '').replace("'", "").replace('+', '')
                            print('Excel_name:::', Excel_name)
                            Product_location_entry.delete(0, END)            
                            Product_location_entry.insert(0, Product_category) 
                            #Create table with excel name
                            cursor = mydb.cursor()
                            # Define the SQL statement to drop the table
                            drop_table_sql = f"DROP TABLE IF EXISTS {DB_table_name}"

                            # Execute the SQL statement to drop the table
                            try:
                                cursor.execute(drop_table_sql)
                                mydb.commit()
                                print(f"Table '{DB_table_name}' deleted successfully.")
                            except mysql.connector.Error as err:
                                print(f"Error: {err}")
                            
                            #---------CREATE TABLE START------------------------
                            # Define the CREATE TABLE statement
                            create_table_sql = """
                            CREATE TABLE IF NOT EXISTS {} (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                product_location VARCHAR(255) CHARACTER SET utf8mb4,
                                product_title VARCHAR(255) CHARACTER SET utf8mb4,
                                product_imgurl VARCHAR(255) CHARACTER SET utf8mb4,
                                product_brand VARCHAR(255) CHARACTER SET utf8mb4,
                                product_rating VARCHAR(255) CHARACTER SET utf8mb4,
                                number_reviews VARCHAR(255) CHARACTER SET utf8mb4,
                                product_price VARCHAR(255) CHARACTER SET utf8mb4,
                                Product_About_Item VARCHAR(255) CHARACTER SET utf8mb4,
                                product_dim VARCHAR(255) CHARACTER SET utf8mb4,
                                product_asin VARCHAR(255) CHARACTER SET utf8mb4,
                                product_modelnumber VARCHAR(255) CHARACTER SET utf8mb4,
                                product_department VARCHAR(255) CHARACTER SET utf8mb4,
                                product_dateavailable VARCHAR(255) CHARACTER SET utf8mb4,
                                Product_Special VARCHAR(255) CHARACTER SET utf8mb4,
                                product_manufacturer VARCHAR(255) CHARACTER SET utf8mb4,
                                product_country VARCHAR(255) CHARACTER SET utf8mb4,
                                upspsc_code VARCHAR(255) CHARACTER SET utf8mb4,
                                product_bsr VARCHAR(255) CHARACTER SET utf8mb4,
                                number_solds VARCHAR(255) CHARACTER SET utf8mb4,
                                product_specification TEXT CHARACTER SET utf8mb4,
                                product_description TEXT CHARACTER SET utf8mb4,
                                timestamp VARCHAR(255) CHARACTER SET utf8mb4,
                                Leaf_Depth VARCHAR(255) CHARACTER SET utf8mb4
                            );
                            """.format(DB_table_name)

                            # Execute the CREATE TABLE statement
                            try:
                                cursor.execute(create_table_sql)
                                # Commit the changes to the database
                                mydb.commit()
                                cursor.close()
                            except:
                                print("creating table error")
                            #---------CREATE TABLE END------------------------
                        
                            dict = {'Product_Location_in_Tree': [], 'Product_title': [], 'Product_image_URL': [], 'Product_brand': [],'Product_Rating': [], 'Number_of_Customer_review': [], 'Product_price': [], 
                            'Product_About_Item': [], 'Product_Dim': [], 'Product_ASIN': [], 'Product_Item_Model_number': [], 'Product_Department': [], 'Product_Date_First_Available': [], 'Product_Special': [],
                            'Product_manufacturer': [], 'Country_Origin': [], 'UPSPSC_Code': [], 'Product_BSR': [], 'Number of sold of in a month': [], 'Product Specification': [], "Product Description": [], "timestamp": [], "Leaf Depth": []}
                            df = pd.DataFrame(dict)
                            df.to_csv(f'{Excel_name}.csv', encoding='utf-8', index=False) 
                            
                            driver.get(URL)  
                            i = 0          

                            tables = driver.find_elements(By.CSS_SELECTOR, Product_tables_CSS_SELECTOR)
                            tables_len = 0
                            while(tables_len != len(tables)):
                                tables_len = len(tables)
                                backtoTop_element = driver.find_element(By.CLASS_NAME, backtoTop_className)
                                driver.execute_script("arguments[0].scrollIntoView(true);", backtoTop_element)
                                time.sleep(5)
                                tables = driver.find_elements(By.CSS_SELECTOR, Product_tables_CSS_SELECTOR)
                                
                            tables = driver.find_elements(By.CSS_SELECTOR, Product_tables_CSS_SELECTOR)
                            print(len(tables))
                            for table in tables:
                                try:                           
                                    if (len(Product_title_list) > int(scan_limit)-1):
                                        break
                                    try:
                                        Product_URL = table.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
                                    except:
                                        Product_URL = "none"
                                    
                                    # Getting the product title
                                    try:
                                        Product_title = table.find_elements(By.TAG_NAME, 'a')[1].find_elements(By.TAG_NAME, 'span')[0].text
                                    except:
                                        Product_title = "none"
                                    
                                    try:
                                        try:
                                            Product_price = table.find_element(By.CLASS_NAME, Product_price_Class1).text
                                        except:
                                            Product_price = table.find_element(By.CLASS_NAME, Product_price_Class2).text                  
                                    except:
                                        Product_price = "none"
                                            
                                    driver1 = webdriver.Chrome(options=chrome_options,seleniumwire_options=proxy_options)
                                    driver1.maximize_window()
                                    driver1.get(Product_URL)  
                                            
                                    Product_URL_entry.delete(0, END)            
                                    Product_URL_entry.insert(0, Product_URL)   
                                            
                                    Product_title_entry.delete(0, END)            
                                    Product_title_entry.insert(0, Product_title)  
                                    
                                    Product_Price_entry.delete(0, END)            
                                    Product_Price_entry.insert(0, Product_price)    
                                        
                                    try:
                                        Product_image_URL = driver1.find_element(By.XPATH, Product_image_URL_XPATH).get_attribute('src')
                                    except:
                                        Product_image_URL = "none"
                                    Product_image_URL_entry.delete(0, END)            
                                    Product_image_URL_entry.insert(0, Product_image_URL)             
                                    try:
                                        Product_brand_text = driver1.find_element(By.XPATH, Product_brand_XPATH).text
                                        Product_brand = "none"
                                        if ("Brand" in Product_brand_text):
                                            Product_brand = str(Product_brand_text).replace('Brand:', '').replace(' ', '')
                                        elif ("Visit" in Product_brand_text):
                                            Product_brand = str(Product_brand_text).replace('Visit the', '').replace(' ', '').replace('Store', '')                
                                    except:
                                        Product_brand = "none"  
                                    Product_Brand_entry.delete(0, END)            
                                    Product_Brand_entry.insert(0, Product_brand)          
                                    
                                    try:
                                        Product_Rate = driver1.find_element(By.XPATH, Product_Rate_XPATH).text
                                    except:
                                        Product_Rate = "none"
                                    Product_Rating_entry.delete(0, END)            
                                    Product_Rating_entry.insert(0, Product_Rate)
                                    
                                    try:
                                        Product_Rating = driver1.find_element(By.XPATH, Product_Rating_XPATH).text
                                    except:
                                        Product_Rating = "none"
                                    Product_Rating = str(Product_Rating).replace('ratings', '').replace(' ', '')
                                    Product_review_entry.delete(0, END)            
                                    Product_review_entry.insert(0, Product_Rating)  
                                    
                                    try:
                                        Product_Month = driver1.find_element(By.XPATH, Product_Month_Sold_XPATH).text
                                        Product_Month = str(Product_Month).replace('bought in past month', '').replace(' ', '')
                                    except:
                                        Product_Month = "none"
                                    
                                    try:
                                        Product_About_Item = driver1.find_element(By.XPATH, Product_About_Item_XPATH).text
                                    except:
                                        Product_About_Item = "none"
                                    
                                    try:
                                        Product_specification = driver1.find_element(By.XPATH, Product_specification_XPATH).get_attribute('innerText')
                                    except:
                                        Product_specification = "none"
                                    
                                    try:
                                        if (len(driver1.find_elements(By.ID, 'productDescription'))>0):
                                            Product_description = driver1.find_element(By.ID, 'productDescription').text
                                        elif (len(driver1.find_elements(By.XPATH, '//*[@id="aplus"]'))>1):
                                            description_details = driver1.find_elements(By.XPATH, '//*[@id="aplus"]')
                                            for description_detail in description_details:
                                                description_text = description_detail.find_element(By.TAG_NAME, 'h2').text
                                                if "Description" in description_text:
                                                    Product_description = description_detail.find_elements(By.TAG_NAME, 'div')[0].text
                                                else:
                                                    Product_description = "none"  
                                        elif (len(driver1.find_elements(By.XPATH, '//*[@id="aplusBatch"]'))>0):
                                            Product_description = driver1.find_element(By.XPATH, '//*[@id="aplusBatch"]').text               
                                        else:
                                            Product_description = "none"
                                    except:
                                        Product_description = "none"
                                    
                                    try:
                                        if (len(driver1.find_elements(By.XPATH, '//*[@id="detailBulletsWrapper_feature_div"]'))>0):
                                            product_detail = driver1.find_element(By.XPATH, '//*[@id="detailBullets_feature_div"]/ul')
                                            firsttables = product_detail.find_elements(By.CLASS_NAME, 'a-list-item')
                                            Product_ASIN = "None"
                                            Product_Dim = "None"
                                            Product_Item = "None"
                                            Product_Department = "none"
                                            Product_Date = "none"
                                            Product_Manu = "none"
                                            Product_Country = "none"
                                            Product_UPSPSC = "none" 
                                            Product_Special = "none"    
                                            for firsttable in firsttables:
                                                item = firsttable.find_element(By.CLASS_NAME, 'a-text-bold').text
                                                # print("item:", item)                
                                                if ("ASIN" in item):
                                                    try:
                                                        Product_ASIN = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_ASIN = "None"
                                                elif ("Dimensions" in item):
                                                    try:
                                                        Product_Dim = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Dim = "None"
                                                elif ("Item model number" in item):
                                                    try:
                                                        Product_Item = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Item = "None"
                                                elif ("Department" in item):
                                                    try:
                                                        Product_Department = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Department = "none"
                                                elif ("Date First Available" in item):
                                                    try:
                                                        Product_Date = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Date = "none"
                                                elif ("Manufacturer" in item):
                                                    try:
                                                        Product_Manu = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Manu = "none"
                                                elif ("Country of Origin" in item):
                                                    try:
                                                        Product_Country = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Country = "none"
                                                elif ("Special" in item):
                                                    try:
                                                        Product_Special = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Special = "none" 
                                                elif ("UPSPSC Code" in item):
                                                    try:
                                                        Product_UPSPSC = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_UPSPSC = "none" 
                                        elif (len(driver1.find_elements(By.XPATH, '//*[@id="prodDetails"]/div/div[1]'))>0):
                                            time.sleep(3)
                                            product_detail = driver1.find_element(By.XPATH, '//*[@id="productDetails_detailBullets_sections1"]/tbody')
                                            firsttables = product_detail.find_elements(By.TAG_NAME, 'tr')
                                            Product_ASIN = "None"
                                            Product_Dim = "None"
                                            Product_Item = "None"
                                            Product_Department = "none"
                                            Product_Date = "none"
                                            Product_Manu = "none"
                                            Product_Country = "none"
                                            Product_UPSPSC = "none"     
                                            Product_Special = "none"
                                            for firsttable in firsttables:
                                                item = firsttable.find_element(By.TAG_NAME, 'th').text
                                                # print("item:", item)                
                                                if ("ASIN" in item):
                                                    try:
                                                        Product_ASIN = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_ASIN = "None"               
                                                elif ("Dimensions" in item):
                                                    try:
                                                        Product_Dim = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Dim = "None"
                                                elif ("Item model number" in item):
                                                    try:
                                                        Product_Item = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Item = "None"
                                                elif ("Department" in item):
                                                    try:
                                                        Product_Department = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Department = "none"
                                                elif ("Date First Available" in item):
                                                    try:
                                                        Product_Date = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Date = "none"
                                                elif ("Manufacturer" in item):
                                                    try:
                                                        Product_Manu = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Manu = "none"
                                                elif ("Country of Origin" in item):
                                                    try:
                                                        Product_Country = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Country = "none"
                                                elif ("Special" in item):
                                                    try:
                                                        Product_Special = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_Special = "none" 
                                                elif ("UPSPSC Code" in item):
                                                    try:
                                                        Product_UPSPSC = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                                                    except:
                                                        Product_UPSPSC = "none"                
                                        else:
                                            Product_ASIN = "none" 
                                            Product_Dim = "none"    
                                            Product_Item = "none"    
                                            Product_Department = "none"    
                                            Product_Date = "none"    
                                            Product_Manu = "none"    
                                            Product_Country = "none"    
                                            Product_UPSPSC = "none"   
                                            Product_Special = "none" 
                                    except:
                                            Product_ASIN = "none" 
                                            Product_Dim = "none"    
                                            Product_Item = "none"    
                                            Product_Department = "none"    
                                            Product_Date = "none"    
                                            Product_Manu = "none"    
                                            Product_Country = "none"    
                                            Product_UPSPSC = "none"   
                                            Product_Special = "none"

                                    Product_asin_entry.delete(0, END)            
                                    Product_asin_entry.insert(0, Product_ASIN)  
                                    Product_dimension_entry.delete(0, END)            
                                    Product_dimension_entry.insert(0, Product_Dim)  
                                    Product_Date_entry.delete(0, END)            
                                    Product_Date_entry.insert(0, Product_Date)                 
                                    Product_timestamp_entry.delete(0, END)            
                                    Product_timestamp_entry.insert(0, timestamp)    
                                    Error_counter_entry.delete(0, END)            
                                    Error_counter_entry.insert(0, error_number)     
                                    i += 1
                                    Product_BSR = "#" + str(i)
                                    Product_BSR_entry.delete(0, END)            
                                    Product_BSR_entry.insert(0, Product_BSR) 
                                    print('Product_BSR:', Product_BSR)                
                                    print('timestamp:', timestamp)
                                    Product_title_list.append(Product_title)     
                                    Product_category_list.append(Product_category)        
                                    Product_image_URL_list.append(Product_image_URL)
                                    Product_brand_list.append(Product_brand)
                                    Product_Rate_list.append(Product_Rate)
                                    Product_Rating_list.append(Product_Rating)
                                    Product_specification_list.append(Product_specification)
                                    Product_description_list.append(Product_description)
                                    Product_price_list.append(Product_price)
                                    Product_Dim_list.append(Product_Dim)
                                    Product_ASIN_list.append(Product_ASIN)
                                    Product_Item_list.append(Product_Item)
                                    Product_Department_list.append(Product_Department)
                                    Product_Date_list.append(Product_Date)
                                    Product_Manu_list.append(Product_Manu)
                                    Product_Special_list.append(Product_Special)
                                    Product_Country_list.append(Product_Country)
                                    Product_UPSPSC_list.append(Product_UPSPSC)
                                    Product_BSR_list.append(Product_BSR)
                                    Product_Month_list.append(Product_Month)
                                    Product_About_Item_list.append(Product_About_Item)
                                    timestamp_list.append(timestamp)
                                    Leaf_depth_list.append(Leaf_Depth)
                                    
                                    insert_sql = f"""INSERT INTO {DB_table_name} (product_location, product_title, product_imgurl, product_brand, product_rating, number_reviews, product_price, Product_About_Item, product_dim, product_asin, product_modelnumber, product_department, product_dateavailable, product_special, product_manufacturer, product_country, upspsc_code, product_bsr,  number_solds, product_specification, product_description, timestamp, Leaf_Depth) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                                    insert_values = [Product_category, Product_title, Product_image_URL, Product_brand, Product_Rate, Product_Rating, Product_price, Product_About_Item, Product_Dim, Product_ASIN, 
                                                    Product_Item, Product_Department, Product_Date, Product_Special, Product_Manu, Product_Country, Product_UPSPSC, Product_BSR, Product_Month, Product_specification, Product_description, timestamp, Leaf_Depth]
                                    try:
                                        mycursor = mydb.cursor()
                                        mycursor.execute(insert_sql, insert_values)
                                        mydb.commit()
                                        print(mycursor.rowcount, "rows were inserted.")
                                    except Exception as e:
                                        print("An error occurred:", str(e))
                                        
                                    #INSERT INTO EXCEL_NME TABLE -------------END------------------------
                                    
                                    dict = {'Product_Location_in_Tree': Product_category_list, 'Product_title': Product_title_list, 'Product_image_URL': Product_image_URL_list, 'Product_brand': Product_brand_list,'Product_Rating': Product_Rate_list, 'Number_of_Customer_review': Product_Rating_list, 'Product_price': Product_price_list, 
                                    'Product_About_Item': Product_About_Item_list, 'Product_Dim': Product_Dim_list, 'Product_ASIN': Product_ASIN_list, 'Product_Item_Model_number': Product_Item_list, 'Product_Department': Product_Department_list, 'Product_Date_First_Available': Product_Date_list, 'Product_Special': Product_Special_list,
                                    'Product_manufacturer': Product_Manu_list, 'Country_Origin': Product_Country_list, 'UPSPSC_Code': Product_UPSPSC_list, 'Product_BSR': Product_BSR_list, 'Number of sold of in a month': Product_Month_list, 'Product Specification': Product_specification_list, "Product Description": Product_description_list, "timestamp": timestamp_list, "Leaf Depth": Leaf_depth_list}
                                    df = pd.DataFrame(dict)
                                    df.to_csv(f'{Excel_name}.csv', encoding='utf-8', index=False)                 
                                    driver1.close()
                                except Exception as e:
                                    print("each product error: ", e)
                                    error_file.write(str(e) + '\n')
                                    error_file.write('\n')
                                    Error_counter_entry.delete(0, END)            
                                    Error_counter_entry.insert(0, e) 
                        except Exception as e:
                            error_number += 1
                            print('error_number::::::::::::::::', error_number)
                            Error_counter_entry.delete(0, END)            
                            Error_counter_entry.insert(0, error_number) 
                            time.sleep(3)
                            continue               
                    
                    driver.close()       
                    print('--------------------Automation scraping is successfully finished--------------------')   
                    # Saving as EXCEL file
                    
                    print('---------------------------Saving result as an Excel--------------------------------')
                    try:
                        print("time_interval: ", time_interval)
                        time.sleep(int(time_interval)*60)
                        print("time finished")
                    except:
                        pass
                except Exception as e:
                    print("error:", e)
                    time.sleep(3)
    finally:
        sys.stdout = original_stdout 
    

# defining the building GUI function

def BuildingGUI():
    global Product_location_entry, Product_URL_entry, Product_Running_entry, Product_title_entry, Product_Price_entry, Product_Brand_entry, Product_Rating_entry, Product_review_entry, Product_BSR_entry, Product_asin_entry, Product_image_URL_entry, Product_dimension_entry, Product_Date_entry, Product_Depth_entry, Product_timestamp_entry, Error_counter_entry
    # Create a window object
    scan_limit = ""
    time_interval = ""

    try:
        df3 = pd.read_csv("configuration.csv")
        Configuration_item_list = df3.Item_text
        Configuration_item_link_list = df3.Item_link

        scan_limit_list = df3.Scan_limit
        time_interval_list = df3.time_interval
        scan_limit = scan_limit_list[0]
        time_interval = time_interval_list[0]

    except:
        pass
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("assets/")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Tk()
    window.title("Crawler")
    window.geometry("+500+100")
    window.geometry("1000x800")
    window.configure(bg = "#202020")
    canvas_width = 1000
    canvas_height = 800
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 800,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    image = Image.open("amazon1-mask.png")
    # image = Image.open("amazon3-mask.png")
    image = image.resize((canvas_width, canvas_height), Image.ANTIALIAS)
    background_image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=background_image)
    canvas.place(x = 0, y = 0)

    # Tree Structure
    canvas.pack()

    # Create a Frame widget to hold the Treeview
    tree_frame = tk.Frame(canvas,  bg="#FFFFFF")
    tree_frame.pack()
    
    vscrollbar = tk.Scrollbar(tree_frame, orient="vertical")
    vscrollbar.pack(side="right", fill="y")
    
    hscrollbar = tk.Scrollbar(tree_frame, orient="horizontal")
    hscrollbar.pack(side="bottom", fill="x")
    

    style = ttk.Style()
    # style.configure("Custom.Treeview",
    #                 background="#233839")
    style.configure("Custom.Treeview",
                    background="#3d2802")

    # Create a Treeview widget inside the Frame
    tree = ttk.Treeview(
        tree_frame,
        # columns=("", "", ""),
        height=30,  # Set the number of visible items
        yscrollcommand=vscrollbar.set,  # Link to the scrollbar
        xscrollcommand=hscrollbar.set,  # Link to the scrollbar
        style="Custom.Treeview",
        selectmode="extended"
    )
    # tree.configure(width=800)
    tree.column("#0", width=350)
    # tree.place(width=800, height=200)
    tree.pack(fill="both", expand=True)
    vscrollbar.config(command=tree.yview)
    hscrollbar.config(command=tree.xview)
    tree.configure(xscrollcommand=hscrollbar.set)
    hscrollbar.configure(command=tree.xview)
    # tree.place(x = -300, y = -200, width=500, height=200)

    # Configure the scrollbar to work with the Treeview
    
    # Getting the treeview text when it's selected
    tree.tag_configure("custom_font", font=("American Typewriter", 12), foreground="white")
    def open_all_items(tree):
    # Get all item IDs in the Treeview
        for item in get_all_children(tree, ""):
            tree.item(item, tags=("custom_font"), open=True)
        # item_ids = tree.get_children()

        # # Open each item by setting its state to "open"
        # for item_id in item_ids:
        #     tree.item(item_id, open=True)
    
    def get_childItems(item):
        global item_link, item_text, Category_result, item_link_list, category_result_list, table_name_list, depth_list
        scan_limit = Product_Depth_entry.get()
        time_interval = Product_Running_entry.get()
        child_items = tree.get_children(item)
        child_len = len(child_items)
        if(child_len != 0):
            for child_item in child_items:
                get_childItems(child_item)
        else:
            parents = []
            item_text = tree.item(item)['text']
            item_link = tree.item(item)['tags']   
            print("item-----------------:", item_link)         
            parent_item = tree.parent(item)
            depth = 0
            while parent_item != '':
                parent_text = tree.item(parent_item, 'text')
                parents.append(parent_text)
                parent_item = tree.parent(parent_item)
                depth +=1
            depth_list.append(depth)
            current_item_text = tree.item(item, 'text')
            parents.insert(0, current_item_text)
            parents.reverse()
            Category_result = ' > '.join(parents)
            item_link_list.append(item_link[0])         
            category_result_list.append(Category_result)
            item_text_0 = item_text.replace(' ', '').replace(',', '').replace('&', '').replace(':', '').replace('-', '').replace("'", "").replace('+', '')
            Category_result_text = Category_result.split('>')[1].replace(' ', '').replace(',', '').replace('&', '').replace('-', '').replace(':', '').replace("'", "").replace('+', '')
            table_name = Category_result_text + '_' + item_text_0
            table_name_list.append(table_name)
            item_text_list.append(item_text)
            dict_0 = {'Item_link': item_link_list, 'Category_result': category_result_list, 'table_name': table_name_list, 'Item_text': item_text_list, 'Scan_limit': scan_limit, 'time_interval': time_interval, 'Depth': depth_list}
            df_0 = pd.DataFrame(dict_0)
            df_0.to_csv('configuration.csv')
            return
            
    def save_config():
        selected_items = tree.selection()
        for selected_item in selected_items:           
            
            try:
                get_childItems(selected_item)            
            except:
                continue
        print("item_link_test")
        print(item_link_list, len(item_link_list))        
        print(category_result_list, len(category_result_list)) 
        print(table_name_list, len(table_name_list))    
    def start_function():                        
        global thread, Product_Depth_entry        
        thread = threading.Thread(target = scrape_site, args=())
        thread.start()
        
    def load_jsonfile():
        parent_item = tree.insert("", "end", text="Any Department")
        with open('result.json', 'r') as file:
            for line in file:
                # Do something with line1 and line2
                line_word = line.strip()
                if(line_word == "back"):
                    # print("back")
                    parent_item = tree.parent(parent_item)    
                else:
                    item = json.loads(line_word)
                    item_text = item['name']
                    item_link = item['link']
                    child_item = tree.insert(parent_item, "end", text=item_text, tag = item_link)
                    parent_item = child_item                   

        file.close()
    
    load_jsonfile()
    open_all_items(tree)
    # Iterate through the items in the tree view
    try:        
        for item in get_all_children(tree, ""):
            # print(item['text'])
            tree.item(item, open=True)        
            item_text = tree.item(item)['text']
            item_link = tree.item(item)['tags']
            length =  len(Configuration_item_list)
            # Check if the item matches the saved information
            for i in range(length):
                selected_item_text = Configuration_item_list[i]
                selected_item_link = Configuration_item_link_list[i]
                if selected_item_link in item_link:
                    # print("selected_item_link:", selected_item_link)
                    parent_item = tree.parent(item)
                    tree.item(parent_item, open=True) 
                    while parent_item:
                        parent_item = tree.parent(parent_item)
                        # print("parent_item: ", tree.item(parent_item)['text'])
                        tree.item(parent_item, open=True)                            
                    tree.selection_add(item)
    except:
        pass

    # Update the canvas window to fit the contents
    tree.update_idletasks()
    canvas.create_window((0, 0), window=tree_frame, anchor="nw")

    # Configure the Canvas to scroll
    canvas.config(scrollregion=canvas.bbox("all"))  

    canvas.create_text(
        400.0,
        45.0,
        anchor="nw",
        text="Product Location",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_location_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_location_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_location_entry.place(
        x=550.0,
        y=43,
        width=400.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        105.0,
        anchor="nw",
        text="Product URL",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_URL_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    Product_URL_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_URL_entry.place(
        x=550.0,
        y=103,
        width=400.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        165.0,
        anchor="nw",
        text="Product title",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_title_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_title_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_title_entry.place(
        x=550.0,
        y=163,
        width=400.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        225.0,
        anchor="nw",
        text="Price",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_Price_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_Price_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_Price_entry.place(
        x=500.0,
        y=223,
        width=150.0,
        height=30.0
    )
    
    canvas.create_text(
        680.0,
        225.0,
        anchor="nw",
        text="Brand",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_Brand_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )
    
    Product_Brand_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_Brand_entry.place(
        x=800.0,
        y=223,
        width=150.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        285.0,
        anchor="nw",
        text="Rating",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_Rating_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_Rating_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_Rating_entry.place(
        x=500.0,
        y=283,
        width=150.0,
        height=30.0
    )
    
    canvas.create_text(
        680.0,
        290.0,
        anchor="nw",
        text="reviewNum",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_review_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_review_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_review_entry.place(
        x=800.0,
        y=283,
        width=150.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        350.0,
        anchor="nw",
        text="BSR",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_BSR_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_BSR_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_BSR_entry.place(
        x=500.0,
        y=343,
        width=150.0,
        height=30.0
    )
    
    canvas.create_text(
        680.0,
        350.0,
        anchor="nw",
        text="ASIN",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_asin_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_asin_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_asin_entry.place(
        x=800.0,
        y=343,
        width=150.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        410.0,
        anchor="nw",
        text="Image URL",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_image_URL_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_image_URL_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_image_URL_entry.place(
        x=550.0,
        y=403,
        width=400.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        470.0,
        anchor="nw",
        text="Dimension",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_dimension_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_dimension_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_dimension_entry.place(
        x=550.0,
        y=463,
        width=400.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        590.0,
        anchor="nw",
        text="Date",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_Date_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_Date_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_Date_entry.place(
        x=500.0,
        y=583,
        width=150.0,
        height=30.0
    )   
    
    canvas.create_text(
        680.0,
        590.0,
        anchor="nw",
        text="ErrorNum",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Error_counter_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Error_counter_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Error_counter_entry.place(
        x=800.0,
        y=583,
        width=150.0,
        height=30.0
    )  
    
    canvas.create_text(
        400.0,
        530.0,
        anchor="nw",
        text="TimeStamp",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_timestamp_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_timestamp_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_timestamp_entry.place(
        x=550.0,
        y=523,
        width=400.0,
        height=30.0
    )
    
    canvas.create_text(
        400.0,
        650.0,
        anchor="nw",
        text="Interval",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_Running_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_Running_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_Running_entry.place(
        x=500.0,
        y=643,
        width=150.0,
        height=30.0
    )
    
    canvas.create_text(
        680.0,
        650.0,
        anchor="nw",
        text="ScanDepth",
        fill="#FFFFFF",
        font=("Comic Sans MS", 18 * -1)
    )
    
    Product_Depth_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0,
        justify="center"
    )

    Product_Depth_entry.configure(font=("Comic Sans MS", 12, "bold"), insertbackground="#ff0000")
    
    Product_Depth_entry.place(
        x=800.0,
        y=643,
        width=150.0,
        height=30.0
    )    
    
    Product_Depth_entry.delete(0, END)            
    Product_Depth_entry.insert(0, scan_limit)
    Product_Running_entry.delete(0, END)            
    Product_Running_entry.insert(0, time_interval)
    
    start_img = PhotoImage(file=relative_to_assets("start.png"))
    start_btn = Button(
        image=start_img, borderwidth=0, highlightthickness=0, relief="flat",command=lambda : start_function(), activebackground= "#202020")
    start_btn.place(x=450, y=720, width=100, height=47)
    
    save_img = PhotoImage(file=relative_to_assets("save.png"))
    save_btn = Button(
        image=save_img, borderwidth=0, highlightthickness=0, relief="flat",command=lambda : save_config(), activebackground= "#202020")
    save_btn.place(x=75, y=720, width=100, height=47)
    
    stop_img = PhotoImage(file=relative_to_assets("stop.png"))    
    stop_btn = Button(image=stop_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : stop_function(), activebackground= "#202020")
    stop_btn.place(x=825, y=720, width=100, height=47)   
    
    # print("Product Category: ", Product_category)
    
    window.resizable(False, False)
    # Run the main event loop to display the window
    window.mainloop()
BuildingGUI()
    

            