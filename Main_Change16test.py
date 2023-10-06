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

# Replace 'your_excel_file.xlsx' with the path to your Excel file
csv_file  = 'Result.csv'

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
category_result_list = []
table_name_list = []
# defining the Scrape function
        
def stop_function():
    print("--------------------Scraping is stopped---------------------------")
    global stop_event
    stop_event = threading.Event()
    stop_event.set()
    
def scrape_site():
    global category_result_list, table_name_list
    global item_link_list
    logging.getLogger('webdriver_manager').disabled = True
    
    SCRAPEOPS_API_KEY = 'ab147e77-85aa-4e7f-8be4-6f1b2a685d62'
            
    proxy_options = {
        'proxy': {
            'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
            'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
            'no_proxy': 'localhost:127.0.0.1'
        }
    }
    
    
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
    
    print('--------------------Automation scraping is successfully started-------------------')
    driver = webdriver.Chrome(seleniumwire_options=proxy_options)        
    driver.maximize_window()
    for k in range(0, len(item_link_list)):
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
        print("k:", k)
        URL = item_link_list[k]
        print("URL:", URL)
        Product_location = category_result_list[k]
        print("Category:", Product_location)
        
        Product_category = Product_location
        Excel_name = str(Product_category).replace(',', '').replace(' ', '').replace('&', '').replace('>', '_')
        
        #Create table with excel name
        cursor = mydb.cursor()
        # Define the SQL statement to drop the table
        drop_table_sql = f"DROP TABLE IF EXISTS {table_name_list[k]}"

        # Execute the SQL statement to drop the table
        try:
            cursor.execute(drop_table_sql)
            print(f"Table '{item_text}' deleted successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        mydb.commit()
        
        #---------CREATE TABLE START------------------------
        # Define the CREATE TABLE statement
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS {} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_location VARCHAR(255),
            product_title VARCHAR(255),
            product_imgurl VARCHAR(255),
            product_brand VARCHAR(255),
            product_rating VARCHAR(255),
            number_reviews VARCHAR(255),
            product_price VARCHAR(255),
            Product_About_Item VARCHAR(255),
            product_dim VARCHAR(255),
            product_asin VARCHAR(255),
            product_modelnumber VARCHAR(255),
            product_department VARCHAR(255),
            product_dateavailable VARCHAR(255),
            Product_Special VARCHAR(255),
            product_manufacturer VARCHAR(255),
            product_country VARCHAR(255),
            upspsc_code VARCHAR(255),
            product_bsr VARCHAR(255),
            number_solds VARCHAR(255),
            product_specification TEXT,
            product_description TEXT
        );
        """.format(table_name_list[k])

        # Execute the CREATE TABLE statement
        
        cursor.execute(create_table_sql)

        # Commit the changes to the database
        mydb.commit()
        cursor.close()
        #---------CREATE TABLE END------------------------
    
        driver.get(URL)  
        i = 0
        tables = driver.find_elements(By.CSS_SELECTOR, Product_tables_CSS_SELECTOR)
        print(len(tables))
        for table in tables:
            try:
                Product_URL = table.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            except:
                Product_URL = "none"
            print("Product_URL:", Product_URL)
            # Getting the product title
            try:
                Product_title = table.find_elements(By.TAG_NAME, 'a')[1].find_elements(By.TAG_NAME, 'span')[0].text
            except:
                Product_title = "none"
            print("Product_title:", Product_title)
            try:
                try:
                    Product_price = table.find_element(By.CLASS_NAME, Product_price_Class1).text
                except:
                    Product_price = table.find_element(By.CLASS_NAME, Product_price_Class2).text                  
            except:
                Product_price = "none"
            print("Product_price:", Product_price)
            
            driver1 = webdriver.Chrome(seleniumwire_options=proxy_options)
            driver1.maximize_window()
            driver1.get(Product_URL)  
                    
            print("Product_category:", Product_category) 
                        
            try:
                Product_image_URL = driver1.find_element(By.XPATH, Product_image_URL_XPATH).get_attribute('src')
            except:
                Product_image_URL = "none"
            print("Product_image_URL:", Product_image_URL)
            
            try:
                Product_brand_text = driver1.find_element(By.XPATH, Product_brand_XPATH).text
                Product_brand = "none"
                if ("Brand" in Product_brand_text):
                    Product_brand = str(Product_brand_text).replace('Brand:', '').replace(' ', '')
                elif ("Visit" in Product_brand_text):
                    Product_brand = str(Product_brand_text).replace('Visit the', '').replace(' ', '').replace('Store', '')                
            except:
                Product_brand = "none"            
            print("Product_brand:", Product_brand)
            
            try:
                Product_Rate = driver1.find_element(By.XPATH, Product_Rate_XPATH).text
            except:
                Product_Rate = "none"
            print("Product_Rate:", Product_Rate)
            
            try:
                Product_Rating = driver1.find_element(By.XPATH, Product_Rating_XPATH).text
            except:
                Product_Rating = "none"
            Product_Rating = str(Product_Rating).replace('ratings', '').replace(' ', '')
            print("Product_Rating:", Product_Rating)  
            
            try:
                Product_Month = driver1.find_element(By.XPATH, Product_Month_Sold_XPATH).text
                Product_Month = str(Product_Month).replace('bought in past month', '').replace(' ', '')
            except:
                Product_Month = "none"
            print("Product_Month:", Product_Month) 
            
            try:
                Product_About_Item = driver1.find_element(By.XPATH, Product_About_Item_XPATH).text
            except:
                Product_About_Item = "none"
            print('Product_About_Item:', Product_About_Item)
            try:
                Product_specification = driver1.find_element(By.XPATH, Product_specification_XPATH).get_attribute('innerText')
            except:
                Product_specification = "none"
            print('Product_specification:', Product_specification)
            
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
            print("Product_description:", Product_description)
            
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
                        print('-------Product Details ASIN------')
                        Product_ASIN = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_ASIN:', Product_ASIN)                    
                    elif ("Dimensions" in item):
                        print('-------Product Details Dim------')
                        Product_Dim = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_Dim:', Product_Dim)
                    elif ("Item model number" in item):
                        print('-------Product Details modelnum------')
                        Product_Item = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_Item:', Product_Item)
                    elif ("Department" in item):
                        print('-------Product Details------')
                        Product_Department = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_Department:', Product_Department)
                    elif ("Date First Available" in item):
                        print('-------Product Details------')
                        Product_Date = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_Date:', Product_Date)
                    elif ("Manufacturer" in item):
                        print('-------Product Details------')
                        Product_Manu = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_Manu:', Product_Manu)
                    elif ("Country of Origin" in item):
                        print('-------Product Details------')
                        Product_Country = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_Country:', Product_Country)
                    elif ("Special" in item):
                        print('-------Product Details------')
                        Product_Special = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_Special:', Product_Special)
                    elif ("UPSPSC Code" in item):
                        print('-------Product Details------')
                        Product_UPSPSC = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                        print('Product_UPSPSC:', Product_UPSPSC)
            elif (len(driver1.find_elements(By.XPATH, '//*[@id="prodDetails"]/div/div[1]'))>0):
                print('------------------------------')
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
                        print('-------Product Details ASIN------')
                        Product_ASIN = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_ASIN:', Product_ASIN)                    
                    elif ("Dimensions" in item):
                        print('-------Product Details Dim------')
                        Product_Dim = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_Dim:', Product_Dim)
                    elif ("Item model number" in item):
                        print('-------Product Details modelnum------')
                        Product_Item = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_Item:', Product_Item)
                    elif ("Department" in item):
                        print('-------Product Details------')
                        Product_Department = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_Department:', Product_Department)
                    elif ("Date First Available" in item):
                        print('-------Product Details------')
                        Product_Date = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_Date:', Product_Date)
                    elif ("Manufacturer" in item):
                        print('-------Product Details------')
                        Product_Manu = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_Manu:', Product_Manu)
                    elif ("Country of Origin" in item):
                        print('-------Product Details------')
                        Product_Country = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_Country:', Product_Country)
                    elif ("Special" in item):
                        print('-------Product Details------')
                        Product_Special = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_Special:', Product_Special)
                    elif ("UPSPSC Code" in item):
                        print('-------Product Details------')
                        Product_UPSPSC = firsttable.find_element(By.TAG_NAME, 'td').text
                        print('Product_UPSPSC:', Product_UPSPSC)                  
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
                    
            i += 1
            Product_BSR = "#" + str(i)
            print('Product_BSR:', Product_BSR)
            
            
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
            
            insert_sql = f"""INSERT INTO {table_name_list[k]} (product_location, product_title, product_imgurl, product_brand, product_rating, number_reviews, product_price, Product_About_Item, product_dim, product_asin, product_modelnumber, product_department, product_dateavailable, product_special, product_manufacturer, product_country, upspsc_code, product_bsr,  number_solds, product_specification, product_description) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            insert_values = [Product_category, Product_title, Product_image_URL, Product_brand, Product_Rate, Product_Rating, Product_price, Product_About_Item, Product_Dim, Product_ASIN, 
                             Product_Item, Product_Department, Product_Date, Product_Special, Product_Manu, Product_Country, Product_UPSPSC, Product_BSR, Product_Month, Product_specification, Product_description]
            print(insert_values)
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
            'Product_manufacturer': Product_Manu_list, 'Country_Origin': Product_Country_list, 'UPSPSC_Code': Product_UPSPSC_list, 'Product_BSR': Product_BSR_list, 'Number of sold of in a month': Product_Month_list, 'Product Specification': Product_specification_list, "Product Description": Product_description_list}
            df = pd.DataFrame(dict)
            df.to_csv(f'{Excel_name}.csv') 
            
            driver1.close()         
       
    print('--------------------Automation scraping is successfully finished--------------------')   
    # Saving as EXCEL file
    
    print('---------------------------Saving result as an Excel--------------------------------')
    
    

# defining the building GUI function

def BuildingGUI():
    # Create a window object
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("assets/")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Tk()
    window.title("Crawler")
    window.geometry("+500+100")
    window.geometry("1000x800")
    window.configure(bg = "#202020")
    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 800,
        width = 1000,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    # Tree Structure
    canvas.pack()

    # Create a Frame widget to hold the Treeview
    tree_frame = tk.Frame(canvas,  bg="#FFFFFF")
    tree_frame.pack()
    vscrollbar = tk.Scrollbar(tree_frame, orient="vertical")
    vscrollbar.pack(side="right", fill="y")

    style = ttk.Style()
    style.configure("Custom.Treeview",
                    background="#FFFFFF")

    # Create a Treeview widget inside the Frame
    tree = ttk.Treeview(
        tree_frame,
        # columns=("", "", ""),
        height=30,  # Set the number of visible items
        yscrollcommand=vscrollbar.set,  # Link to the scrollbar
        style="Custom.Treeview"
    )

    # tree.place(width=400, height=200)
    tree.pack(fill="both", expand=True)
    # tree.place(x = -300, y = -200, width=500, height=200)

    # Configure the scrollbar to work with the Treeview
    vscrollbar.config(command=tree.yview)
    # Getting the treeview text when it's selected
        
    def start_function():
        global item_link, item_text, Category_result, item_link_list, category_result_list, table_name_list          
        selected_items = tree.selection()
        for selected_item in selected_items:            
            
            child_items = tree.get_children(selected_item)
            if len(child_items):               
                for child_item in child_items:
                    parents1 = []
                    child_item_text = tree.item(child_item, "text")
                    child_item_tags = str(tree.item(child_item, "tags")).replace('(', '').replace(')', '').replace(',', '').replace("'", "")
                    parent_item = tree.parent(child_item)
                    while parent_item != '':
                        parent_text = tree.item(parent_item, 'text')
                        parents1.append(parent_text)
                        parent_item = tree.parent(parent_item)
                    current_item_text = tree.item(child_item, 'text')
                    parents1.insert(0, current_item_text)
                    parents1.reverse()
                    Category_result = ' > '.join(parents1)
                    item_link_list.append(child_item_tags)
                    category_result_list.append(Category_result)
                    item_text_0 = child_item_text.replace(' ', '').replace(',', '').replace('&', '')
                    Category_result_text = Category_result.split('>')[0].replace(' ', '').replace(',', '').replace('&', '')
                    table_name = Category_result_text + '_' + item_text_0
                    table_name_list.append(table_name)
            else:
                parents = []
                item_text = tree.item(selected_item)['text']
                item_link = tree.item(selected_item)['tags']            
                parent_item = tree.parent(selected_item)
                while parent_item != '':
                    parent_text = tree.item(parent_item, 'text')
                    parents.append(parent_text)
                    parent_item = tree.parent(parent_item)
                current_item_text = tree.item(selected_item, 'text')
                parents.insert(0, current_item_text)
                parents.reverse()
                Category_result = ' > '.join(parents)
                item_link_list.append(item_link[0])
                category_result_list.append(Category_result)
                item_text_0 = item_text.replace(' ', '').replace(',', '').replace('&', '')
                Category_result_text = Category_result.split('>')[0].replace(' ', '').replace(',', '').replace('&', '')
                table_name = Category_result_text + '_' + item_text_0
                table_name_list.append(table_name)
        print(item_link_list)
        print(category_result_list) 
        print(table_name_list)               
        global thread
        thread = threading.Thread(target = scrape_site, args=())
        thread.start()
    
    # Amazon Devices & Accessories
    parent_item = tree.insert("", "end", text="Amazon Devices & Accessories")
    child_1 = tree.insert(parent_item, "end", text="Amazon Device Accessories")
    tree.insert(child_1, "end", text="Adapters & Connectors", tag="https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Adapters-Connectors/zgbs/amazon-devices/17942903011/ref=zg_bs_nav_amazon-devices_2_370783011")
    tree.insert(child_1, "end", text="Audio", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Audio-Accessories/zgbs/amazon-devices/1289283011/ref=zg_bs_nav_amazon-devices_2_17942903011')
    tree.insert(child_1, "end", text="Bases & Stands", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Bases-Stands/zgbs/amazon-devices/16956974011/ref=zg_bs_nav_amazon-devices_2_1289283011')
    tree.insert(child_1, "end", text="Charging Docks", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Charging-Docks/zgbs/amazon-devices/23673183011/ref=zg_bs_nav_amazon-devices_2_16956974011')
    tree.insert(child_1, "end", text="Clocks", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Clocks/zgbs/amazon-devices/21579956011/ref=zg_bs_nav_amazon-devices_2_23673183011')
    tree.insert(child_1, "end", text="Covers", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Device-Covers/zgbs/amazon-devices/1288346011/ref=zg_bs_nav_amazon-devices_2_21579956011')
    tree.insert(child_1, "end", text="Gaming Controllers", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Gaming-Controllers/zgbs/amazon-devices/23673182011/ref=zg_bs_nav_amazon-devices_2_1288346011')
    tree.insert(child_1, "end", text="Home Security Decals & Signs", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Home-Security-Decals-Signs/zgbs/amazon-devices/17942905011/ref=zg_bs_nav_amazon-devices_2_23673182011')
    tree.insert(child_1, "end", text="Home Security Solar Chargers", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Home-Security-Solar-Chargers/zgbs/amazon-devices/23581299011/ref=zg_bs_nav_amazon-devices_2_17942905011')
    tree.insert(child_1, "end", text="Keyboards", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Keyboards/zgbs/amazon-devices/16958810011/ref=zg_bs_nav_amazon-devices_2_23581299011')
    tree.insert(child_1, "end", text="Memory Cards", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Memory-Cards/zgbs/amazon-devices/10871379011/ref=zg_bs_nav_amazon-devices_2_16958810011')
    tree.insert(child_1, "end", text="Mounts", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Mounts/zgbs/amazon-devices/16956975011/ref=zg_bs_nav_amazon-devices_2_10871379011')
    tree.insert(child_1, "end", text="Power Supplies & Chargers", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Power-Supplies-Chargers/zgbs/amazon-devices/1289282011/ref=zg_bs_nav_amazon-devices_2_16956975011')
    tree.insert(child_1, "end", text="Projection Mats", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Projection-Mats/zgbs/amazon-devices/23611967011/ref=zg_bs_nav_amazon-devices_2_1289282011')
    tree.insert(child_1, "end", text="Protection Plans", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-All-Kindle-Protection-Plans/zgbs/amazon-devices/1292074011/ref=zg_bs_nav_amazon-devices_2_23611967011')
    tree.insert(child_1, "end", text="Reading Lights", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-All-Kindle-Reading-Lights/zgbs/amazon-devices/1289281011/ref=zg_bs_nav_amazon-devices_2_1292074011')
    tree.insert(child_1, "end", text="Remote Controls", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Remote-Controls/zgbs/amazon-devices/16926004011/ref=zg_bs_nav_amazon-devices_2_1289281011')
    tree.insert(child_1, "end", text="Screen Protectors", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Kindle-Screen-Protectors/zgbs/amazon-devices/2642143011/ref=zg_bs_nav_amazon-devices_2_16926004011')
    tree.insert(child_1, "end", text="Skins", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-All-Kindle-Skins/zgbs/amazon-devices/1288347011/ref=zg_bs_nav_amazon-devices_2_2642143011')
    tree.insert(child_1, "end", text="Sleeves", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-All-Kindle-Sleeves/zgbs/amazon-devices/2641859011/ref=zg_bs_nav_amazon-devices_2_1288347011')
    tree.insert(child_1, "end", text="Styluses", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Kindle-Styluses/zgbs/amazon-devices/5499877011/ref=zg_bs_nav_amazon-devices_2_2641859011')
    tree.insert(child_1, "end", text="Tangrams", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Tangrams/zgbs/amazon-devices/23611969011/ref=zg_bs_nav_amazon-devices_2_5499877011')
    child_2 = tree.insert(parent_item, "end", text="Amazon Devices")
    tree.insert(child_2, "end", text="Astro Household Robots", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Astro-Household-Robots/zgbs/amazon-devices/23612137011/ref=zg_bs_nav_amazon-devices_2_2102313011')
    tree.insert(child_2, "end", text="Car Dash Cameras", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Car-Dash-Cameras/zgbs/amazon-devices/23747356011/ref=zg_bs_nav_amazon-devices_2_23612137011')
    child_2_0 = tree.insert(child_2, "end", text="Device Bundles")
    tree.insert(child_2_0, "end", text="Echo Smart Speaker & Display Bundles", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Echo-Smart-Speaker-Display-Bundles/zgbs/amazon-devices/17142716011/ref=zg_bs_nav_amazon-devices_3_16926003011')
    tree.insert(child_2_0, "end", text="Fire TV Bundles", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Fire-TV-Bundles/zgbs/amazon-devices/17142717011/ref=zg_bs_nav_amazon-devices_3_17142716011')
    tree.insert(child_2_0, "end", text="Fire Tablet Bundles", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Fire-Tablet-Bundles/zgbs/amazon-devices/17142718011/ref=zg_bs_nav_amazon-devices_3_17142717011')
    tree.insert(child_2_0, "end", text="Home Security from Amazon Bundles", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Key-Home-Kit-Bundles/zgbs/amazon-devices/17900247011/ref=zg_bs_nav_amazon-devices_3_17142718011')
    tree.insert(child_2_0, "end", text="Home Wi-Fi & Networking Bundles", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Home-Wi-Fi-Networking-Bundles/zgbs/amazon-devices/21579963011/ref=zg_bs_nav_amazon-devices_3_17900247011')
    tree.insert(child_2_0, "end", text="Kindle E-reader Bundles", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Kindle-E-reader-Bundles/zgbs/amazon-devices/17142719011/ref=zg_bs_nav_amazon-devices_3_21579963011')
    tree.insert(child_2_0, "end", text="Smart Appliance Bundles", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Appliance-Bundles/zgbs/amazon-devices/21579961011/ref=zg_bs_nav_amazon-devices_3_17142719011')
    tree.insert(child_2_0, "end", text="Wearable Technology Bundles", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Wearable-Technology-Bundles/zgbs/amazon-devices/21579962011/ref=zg_bs_nav_amazon-devices_3_21579961011')
    child_2_1 = tree.insert(child_2, "end", text="Echo Smart Speakers & Displays")
    tree.insert(child_2_1, "end", text="Receivers & Amplifiers", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Receivers-Amplifiers/zgbs/amazon-devices/21579966011/ref=zg_bs_nav_amazon-devices_3_9818047011')
    tree.insert(child_2_1, "end", text="Smart Displays", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Displays/zgbs/amazon-devices/21579965011/ref=zg_bs_nav_amazon-devices_3_21579966011')
    tree.insert(child_2_1, "end", text="Smart Home Controls", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Home-Controls/zgbs/amazon-devices/119148199011/ref=zg_bs_nav_amazon-devices_3_21579965011')
    tree.insert(child_2_1, "end", text="Smart Speakers", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Speakers/zgbs/amazon-devices/21579964011/ref=zg_bs_nav_amazon-devices_3_119148199011')
    child_2_2 = tree.insert(child_2, "end", text="Fire TV")
    tree.insert(child_2_2, "end", text="Smart TVs", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-TVs/zgbs/amazon-devices/21579968011/ref=zg_bs_nav_amazon-devices_3_21579967011')
    tree.insert(child_2_2, "end", text="Soundbars", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Soundbars/zgbs/amazon-devices/119130818011/ref=zg_bs_nav_amazon-devices_3_21579968011')
    tree.insert(child_2_2, "end", text="Streaming Devices", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Streaming-Devices/zgbs/amazon-devices/21579967011/ref=zg_bs_nav_amazon-devices_3_119130818011')
    tree.insert(child_2, "end", text="Fire Tablets", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Fire-Tablets/zgbs/amazon-devices/6669703011/ref=zg_bs_nav_amazon-devices_2_2102313011')
    tree.insert(child_2, "end", text="Home Wi-Fi & Networking", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Home-Wi-Fi-Networking/zgbs/amazon-devices/21579960011/ref=zg_bs_nav_amazon-devices_2_6669703011')
    tree.insert(child_2, "end", text="Kindle E-readers", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Kindle-E-readers/zgbs/amazon-devices/6669702011/ref=zg_bs_nav_amazon-devices_2_21579960011')
    tree.insert(child_2, "end", text="Programmable Devices", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Programmable-Devices/zgbs/amazon-devices/21579957011/ref=zg_bs_nav_amazon-devices_2_6669702011')
    tree.insert(child_2, "end", text="Sleep Trackers", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Sleep-Trackers/zgbs/amazon-devices/24231642011/ref=zg_bs_nav_amazon-devices_2_21579957011')
    tree.insert(child_2, "end", text="Smart Appliances", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Appliances/zgbs/amazon-devices/21579959011/ref=zg_bs_nav_amazon-devices_2_24231642011')
    child_2_3 = tree.insert(child_2, "end", text="Smart Home Security & Lighting")
    tree.insert(child_2_3, "end", text="Alarm Systems", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Alarm-Systems/zgbs/amazon-devices/21579972011/ref=zg_bs_nav_amazon-devices_3_17386948011')
    tree.insert(child_2_3, "end", text="Doorbells & Chimes", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Doorbells-Chimes/zgbs/amazon-devices/21579969011/ref=zg_bs_nav_amazon-devices_3_21579972011')
    tree.insert(child_2_3, "end", text="Motion Detectors", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Motion-Detectors/zgbs/amazon-devices/21579970011/ref=zg_bs_nav_amazon-devices_3_21579969011')
    tree.insert(child_2_3, "end", text="Security Cameras", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Security-Cameras/zgbs/amazon-devices/21579975011/ref=zg_bs_nav_amazon-devices_3_21579970011')
    tree.insert(child_2_3, "end", text="Sensors", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Sensors/zgbs/amazon-devices/21579974011/ref=zg_bs_nav_amazon-devices_3_21579975011')
    child_2_3_0 = tree.insert(child_2_3, "end", text="Smart Lighting")
    tree.insert(child_2_3_0, "end", text="Smart Light Bulbs", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Light-Bulbs/zgbs/amazon-devices/21579977011/ref=zg_bs_nav_amazon-devices_4_21579973011')
    tree.insert(child_2_3_0, "end", text="Smart Light Switches", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Light-Switches/zgbs/amazon-devices/21579978011/ref=zg_bs_nav_amazon-devices_4_21579977011')
    tree.insert(child_2_3_0, "end", text="Smart Outdoor Lighting", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Outdoor-Lighting/zgbs/amazon-devices/21579976011/ref=zg_bs_nav_amazon-devices_4_21579978011')
    tree.insert(child_2_3, "end", text="Smart Locks", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Smart-Locks/zgbs/amazon-devices/17295887011/ref=zg_bs_nav_amazon-devices_3_17386948011')
    tree.insert(child_2_3, "end", text="Smart Plugs", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Plugs/zgbs/amazon-devices/21579971011/ref=zg_bs_nav_amazon-devices_3_17295887011')
    child_2_4 = tree.insert(child_2, "end", text="Wearable Technology")
    tree.insert(child_2_4, "end", text="Earbuds", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Earbuds/zgbs/amazon-devices/23673186011/ref=zg_bs_nav_amazon-devices_3_23673188011')
    tree.insert(child_2_4, "end", text="Smart Wristbands", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smart-Wristbands/zgbs/amazon-devices/23673187011/ref=zg_bs_nav_amazon-devices_3_23673186011')
    tree.insert(child_2_4, "end", text="Smartglasses", tags='https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Smartglasses/zgbs/amazon-devices/23673188011/ref=zg_bs_nav_amazon-devices_3_23673187011')

    #Amazon Renewed
    parent_item1 = tree.insert("", "end", text="Amazon Renewed", tags='https://www.amazon.com/Best-Sellers-Amazon-Renewed/zgbs/amazon-renewed/ref=zg_bs_nav_amazon-renewed_0')


    #Appliances
    parent_item2 = tree.insert("", "end", text="Appliances")
    tree.insert(parent_item2, "end", text="Appliance Warranties", tags='https://www.amazon.com/Best-Sellers-Appliances-Home-Appliance-Warranties/zgbs/appliances/2242350011/ref=zg_bs_nav_appliances_1')
    tree.insert(parent_item2, "end", text="Cooktops", tags='https://www.amazon.com/Best-Sellers-Appliances-Cooktops/zgbs/appliances/3741261/ref=zg_bs_nav_appliances_1_2242350011')
    child2_0 = tree.insert(parent_item2, "end", text="Dishwashers")
    tree.insert(child2_0, "end", text="Built-In Dishwashers", tags='https://www.amazon.com/Best-Sellers-Appliances-Built-In-Dishwashers/zgbs/appliances/3741281/ref=zg_bs_nav_appliances_2_19201449011')
    tree.insert(child2_0, "end", text="Countertop Dishwashers", tags='https://www.amazon.com/Best-Sellers-Appliances-Countertop-Dishwashers/zgbs/appliances/19201451011/ref=zg_bs_nav_appliances_2_3741281')
    tree.insert(child2_0, "end", text="Portable Dishwashers", tags='https://www.amazon.com/Best-Sellers-Appliances-Portable-Dishwashers/zgbs/appliances/19201449011/ref=zg_bs_nav_appliances_2_19201451011')
    child2_1 = tree.insert(parent_item2, "end", text="Freezers")
    tree.insert(child2_1, "end", text="Chest Freezers", tags='https://www.amazon.com/Best-Sellers-Appliances-Chest-Freezers/zgbs/appliances/3741341/ref=zg_bs_nav_appliances_2_3741351')
    tree.insert(child2_1, "end", text="Upright Freezers", tags='https://www.amazon.com/Best-Sellers-Appliances-Upright-Freezers/zgbs/appliances/3741351/ref=zg_bs_nav_appliances_2_3741341')
    tree.insert(parent_item2, "end", text="Ice Makers", tags='https://www.amazon.com/Best-Sellers-Appliances-Ice-Makers/zgbs/appliances/2399939011/ref=zg_bs_nav_appliances_1')
    tree.insert(parent_item2, "end", text="Range Hoods", tags='https://www.amazon.com/Best-Sellers-Appliances-Range-Hoods/zgbs/appliances/3741441/ref=zg_bs_nav_appliances_1_2399939011')
    child2_2 = tree.insert(parent_item2, "end", text="Ranges")
    tree.insert(child2_2, "end", text="Drop-In Ranges", tags='https://www.amazon.com/Best-Sellers-Appliances-Drop-In-Ranges/zgbs/appliances/3741421/ref=zg_bs_nav_appliances_2_3741411')
    tree.insert(child2_2, "end", text="Freestanding Ranges", tags='https://www.amazon.com/Best-Sellers-Appliances-Freestanding-Ranges/zgbs/appliances/3741431/ref=zg_bs_nav_appliances_2_3741421')
    tree.insert(child2_2, "end", text="Slide-In Ranges", tags='https://www.amazon.com/Best-Sellers-Appliances-Slide-In-Ranges/zgbs/appliances/2399946011/ref=zg_bs_nav_appliances_2_3741431')
    tree.insert(parent_item2, "end", text="Refrigerators", tags='https://www.amazon.com/Best-Sellers-Appliances-Refrigerators/zgbs/appliances/3741361/ref=zg_bs_nav_appliances_1')
    child2_3 = tree.insert(parent_item2, "end", text="Wall Ovens")
    tree.insert(child2_3, "end", text="Combination Microwave & Wall Ovens", tags='https://www.amazon.com/Best-Sellers-Appliances-Combination-Microwave-Wall-Ovens/zgbs/appliances/3741491/ref=zg_bs_nav_appliances_2_3741481')
    tree.insert(child2_3, "end", text="Double Wall Ovens", tags='https://www.amazon.com/Best-Sellers-Appliances-Double-Wall-Ovens/zgbs/appliances/3741501/ref=zg_bs_nav_appliances_2_3741491')
    tree.insert(child2_3, "end", text="Single Wall Ovens", tags='https://www.amazon.com/Best-Sellers-Appliances-Single-Wall-Ovens/zgbs/appliances/3741511/ref=zg_bs_nav_appliances_2_3741501')
    tree.insert(parent_item2, "end", text="Warming Drawers", tags='https://www.amazon.com/Best-Sellers-Appliances-Warming-Drawers/zgbs/appliances/2399955011/ref=zg_bs_nav_appliances_1')
    child2_4 = tree.insert(parent_item2, "end", text="Washers & Dryers")
    tree.insert(child2_4, "end", text="All-in-One Combination Washers & Dryers", tags='https://www.amazon.com/Best-Sellers-Appliances-Combination-Washers-Dryers/zgbs/appliances/13755271/ref=zg_bs_nav_appliances_2_2383576011')
    tree.insert(child2_4, "end", text="Dryers", tags='https://www.amazon.com/Best-Sellers-Appliances-Clothes-Dryers/zgbs/appliances/13397481/ref=zg_bs_nav_appliances_2_13755271')
    tree.insert(child2_4, "end", text="Portable Dryers", tags='https://www.amazon.com/Best-Sellers-Appliances-Portable-Dryers/zgbs/appliances/21490694011/ref=zg_bs_nav_appliances_2_13397481')
    tree.insert(child2_4, "end", text="Portable Washers", tags='https://www.amazon.com/Best-Sellers-Appliances-Portable-Clothes-Washing-Machines/zgbs/appliances/9709422011/ref=zg_bs_nav_appliances_2_21490694011')
    tree.insert(child2_4, "end", text="Stacked Washer & Dryer Units", tags='https://www.amazon.com/Best-Sellers-Appliances-Stacked-Washer-Dryer-Units/zgbs/appliances/2399957011/ref=zg_bs_nav_appliances_2_9709422011')
    tree.insert(child2_4, "end", text="Washers", tags='https://www.amazon.com/Best-Sellers-Appliances-Clothes-Washing-Machines/zgbs/appliances/13397491/ref=zg_bs_nav_appliances_2_2399957011')    
    child2_5 = tree.insert(parent_item2, "end", text="Wine Cellars")
    tree.insert(child2_5, "end", text="Built-In Wine Cellars",tags='https://www.amazon.com/Best-Sellers-Kitchen-Dining-Built-In-Wine-Cellars/zgbs/kitchen/3741551/ref=zg_bs_nav_kitchen_3_3741521')
    tree.insert(child2_5, "end", text="Freestanding Wine Cellars", tags='https://www.amazon.com/Best-Sellers-Kitchen-Dining-Freestanding-Wine-Cellars/zgbs/kitchen/3741541/ref=zg_bs_nav_kitchen_3_3741551')
    tree.insert(child2_5, "end", text="Wine Cellar Cooling Systems", tags='https://www.amazon.com/Best-Sellers-Kitchen-Dining-Wine-Cellar-Cooling-Systems/zgbs/kitchen/3741581/ref=zg_bs_nav_kitchen_3_3741541')

    parent_item3 = tree.insert("", "end", text="Apps & Games")
    child3_1 = tree.insert(parent_item3, "end", text="Books & Comics")
    tree.insert(child3_1, "end", text="Book Info & Reviews", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Book-Info-Reviews/zgbs/mobile-apps/9408446011/ref=zg_bs_nav_mobile-apps_2_9408445011')
    tree.insert(child3_1, "end", text="Readers & Players", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Book-Readers-Players/zgbs/mobile-apps/9408445011/ref=zg_bs_nav_mobile-apps_2_9408446011')
    child3_2 = tree.insert(parent_item3, "end", text="Business")
    tree.insert(child3_2, "end", text="Accounting & Expenses", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Accounting-Expenses/zgbs/mobile-apps/9408434011/ref=zg_bs_nav_mobile-apps_2_10298305011')
    tree.insert(child3_2, "end", text="Banking", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Banking/zgbs/mobile-apps/9408435011/ref=zg_bs_nav_mobile-apps_2_9408434011')
    tree.insert(child3_2, "end", text="Currency Converters & Guides", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Currency-Converters-Guides/zgbs/mobile-apps/9408436011/ref=zg_bs_nav_mobile-apps_2_9408435011')
    tree.insert(child3_2, "end", text="Payments & Money Transfers", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Payments-Money-Transfers/zgbs/mobile-apps/9408440011/ref=zg_bs_nav_mobile-apps_2_9408436011')
    tree.insert(child3_2, "end", text="Personal Finance", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Personal-Finance/zgbs/mobile-apps/9408441011/ref=zg_bs_nav_mobile-apps_2_9408440011')
    tree.insert(child3_2, "end", text="Stocks & Investing", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Stocks-Investing/zgbs/mobile-apps/9408438011/ref=zg_bs_nav_mobile-apps_2_9408441011')
    tree.insert(child3_2, "end", text="Tax Calculators", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Tax-Calculators/zgbs/mobile-apps/9408442011/ref=zg_bs_nav_mobile-apps_2_9408438011')
    child3_3 = tree.insert(parent_item3, "end", text="Communication", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Communication/zgbs/mobile-apps/9408466011/ref=zg_bs_nav_mobile-apps_1')
    child3_4 = tree.insert(parent_item3, "end", text="Customization")
    tree.insert(child3_4, "end", text="Ringtones & Notifications", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Ringtones-Notifications/zgbs/mobile-apps/9408485011/ref=zg_bs_nav_mobile-apps_2_9408481011')
    tree.insert(child3_4, "end", text="Themes", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Themes/zgbs/mobile-apps/9408486011/ref=zg_bs_nav_mobile-apps_2_9408485011')
    tree.insert(child3_4, "end", text="Wallpapers & Images", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Wallpapers-Images/zgbs/mobile-apps/9408487011/ref=zg_bs_nav_mobile-apps_2_9408486011')
    tree.insert(child3_4, "end", text="Widgets", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Widgets/zgbs/mobile-apps/9408942011/ref=zg_bs_nav_mobile-apps_2_9408487011')
    child3_5 = tree.insert(parent_item3, "end", text="Education", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Education/zgbs/mobile-apps/9408490011/ref=zg_bs_nav_mobile-apps_1')
    child3_6 = tree.insert(parent_item3, "end", text="Finance")
    tree.insert(child3_6, "end", text="Accounting & Expenses", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Accounting-Expenses/zgbs/mobile-apps/9408434011/ref=zg_bs_nav_mobile-apps_2_9408433011')
    tree.insert(child3_6, "end", text="Banking", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Banking/zgbs/mobile-apps/9408435011/ref=zg_bs_nav_mobile-apps_2_9408434011')
    tree.insert(child3_6, "end", text="Currency Converters & Guides", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Currency-Converters-Guides/zgbs/mobile-apps/9408436011/ref=zg_bs_nav_mobile-apps_2_9408435011')
    tree.insert(child3_6, "end", text="Payments & Money Transfers", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Payments-Money-Transfers/zgbs/mobile-apps/9408440011/ref=zg_bs_nav_mobile-apps_2_9408436011')
    tree.insert(child3_6, "end", text="Personal Finance", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Personal-Finance/zgbs/mobile-apps/9408441011/ref=zg_bs_nav_mobile-apps_2_9408440011')
    tree.insert(child3_6, "end", text="Stocks & Investing", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Stocks-Investing/zgbs/mobile-apps/9408438011/ref=zg_bs_nav_mobile-apps_2_9408441011')
    tree.insert(child3_6, "end", text="Tax Calculators", tags='https://www.amazon.com/Best-Sellers-Apps-Games-Tax-Calculators/zgbs/mobile-apps/9408442011/ref=zg_bs_nav_mobile-apps_2_9408438011')
    child3_7 = tree.insert(parent_item3, "end", text="Food & Drink")
    tree.insert(child3_7, "end", text="Cooking & Recipes")
    tree.insert(child3_7, "end", text="Wine & Beverages")
    child3_8 = tree.insert(parent_item3, "end", text="Games")
    tree.insert(child3_8, "end", text="Action")
    tree.insert(child3_8, "end", text="Adventure")
    tree.insert(child3_8, "end", text="Arcade")
    tree.insert(child3_8, "end", text="Board")
    tree.insert(child3_8, "end", text="Brain & Puzzle")
    tree.insert(child3_8, "end", text="Cards")
    tree.insert(child3_8, "end", text="Casino")
    tree.insert(child3_8, "end", text="Dice")
    tree.insert(child3_8, "end", text="Music & Rhythm")
    tree.insert(child3_8, "end", text="Racing")
    tree.insert(child3_8, "end", text="Role Playing")
    tree.insert(child3_8, "end", text="Seek & Find")
    tree.insert(child3_8, "end", text="Simulation")
    tree.insert(child3_8, "end", text="Sports Games")
    tree.insert(child3_8, "end", text="Strategy")
    tree.insert(child3_8, "end", text="Trivia")
    tree.insert(child3_8, "end", text="Words")
    child3_9 = tree.insert(parent_item3, "end", text="Health & Fitness")
    tree.insert(child3_9, "end", text="Activity Tracking")
    tree.insert(child3_9, "end", text="Exercise Motivation")
    tree.insert(child3_9, "end", text="Heart Rate Monitors")
    tree.insert(child3_9, "end", text="Massage Guides")
    tree.insert(child3_9, "end", text="Meditation Guides")
    tree.insert(child3_9, "end", text="Menstrual Trackers")
    tree.insert(child3_9, "end", text="Nutrition & Diet")
    tree.insert(child3_9, "end", text="Pregnancy")
    tree.insert(child3_9, "end", text="Sleep Tracking")
    tree.insert(child3_9, "end", text="Sounds & Relaxation")
    tree.insert(child3_9, "end", text="Workout Guides")
    tree.insert(child3_9, "end", text="Yoga Guides")
    child3_10 = tree.insert(parent_item3, "end", text="Kids")
    tree.insert(child3_10, "end", text="Book Readers & Players")
    tree.insert(child3_10, "end", text="Education")
    tree.insert(child3_10, "end", text="Games")
    tree.insert(child3_10, "end", text="Movie & TV Streaming")
    tree.insert(child3_10, "end", text="Music & Audio")
    child3_11 = tree.insert(parent_item3, "end", text="Lifestyle")
    tree.insert(child3_11, "end", text="Astrology")
    tree.insert(child3_11, "end", text="Beauty & Cosmetics")
    tree.insert(child3_11, "end", text="Celebrities")
    tree.insert(child3_11, "end", text="Cooking & Recipes")
    tree.insert(child3_11, "end", text="Crafts & DIY")
    tree.insert(child3_11, "end", text="Creative Writing")
    tree.insert(child3_11, "end", text="Diaries")
    tree.insert(child3_11, "end", text="Fashion & Style")
    tree.insert(child3_11, "end", text="Game Rules")
    tree.insert(child3_11, "end", text="Health & Fitness")
    tree.insert(child3_11, "end", text="Home & Garden")
    tree.insert(child3_11, "end", text="Meditation Guides")
    tree.insert(child3_11, "end", text="Outdoors & Nature")
    tree.insert(child3_11, "end", text="Parenting")
    tree.insert(child3_11, "end", text="Pets & Animals")
    tree.insert(child3_11, "end", text="Quotes")
    tree.insert(child3_11, "end", text="Relationships")
    tree.insert(child3_11, "end", text="Religion & Spirituality")
    tree.insert(child3_11, "end", text="Self Improvement")
    tree.insert(child3_11, "end", text="Sexuality")
    tree.insert(child3_11, "end", text="Tattoos & Body Piercing")
    tree.insert(child3_11, "end", text="Wedding")
    tree.insert(child3_11, "end", text="Wine & Beverages")
    child3_12 = tree.insert(parent_item3, "end", text="Local")
    tree.insert(child3_12, "end", text="Business Locators")
    tree.insert(child3_12, "end", text="Navigation")
    tree.insert(child3_12, "end", text="Offline Maps")
    tree.insert(child3_12, "end", text="Real Estate")
    tree.insert(child3_12, "end", text="Taxi & Ridesharing")
    child3_13 = tree.insert(parent_item3, "end", text="Magazines")
    child3_14 = tree.insert(parent_item3, "end", text="Medical")
    tree.insert(child3_14, "end", text="Education")
    tree.insert(child3_14, "end", text="Heart Rate Monitors")
    tree.insert(child3_14, "end", text="Massage Guides")
    tree.insert(child3_14, "end", text="Menstrual Trackers")
    tree.insert(child3_14, "end", text="Pregnancy")
    tree.insert(child3_14, "end", text="Reference")
    tree.insert(child3_14, "end", text="Sleep Tracking")
    child3_15 = tree.insert(parent_item3, "end", text="Movies & TV")
    tree.insert(child3_15, "end", text="Movie Info & Reviews")
    tree.insert(child3_15, "end", text="On-Demand Movie Streaming")
    tree.insert(child3_15, "end", text="Video-Sharing")
    child3_16 = tree.insert(parent_item3, "end", text="Music & Audio")
    tree.insert(child3_16, "end", text="Audio Recording")
    tree.insert(child3_16, "end", text="Instruments & Music Makers")
    tree.insert(child3_16, "end", text="Music Info & Reviews")
    tree.insert(child3_16, "end", text="Music Players")
    tree.insert(child3_16, "end", text="On-Demand Music Streaming")
    tree.insert(child3_16, "end", text="Podcasts")
    tree.insert(child3_16, "end", text="Radio Webcasts")
    tree.insert(child3_16, "end", text="Readers & Players")
    tree.insert(child3_16, "end", text="Ringtones & Notifications")
    tree.insert(child3_16, "end", text="Songbooks & Sheet Music")
    tree.insert(child3_16, "end", text="Sounds & Relaxation")
    child3_17 = tree.insert(parent_item3, "end", text="News")
    tree.insert(child3_17, "end", text="Feed Aggregators")
    tree.insert(child3_17, "end", text="Newspapers")
    tree.insert(child3_17, "end", text="Sports Fan News")
    child3_18 = tree.insert(parent_item3, "end", text="Novelty")
    tree.insert(child3_18, "end", text="Funny Pictures")
    tree.insert(child3_18, "end", text="Funny Sounds")
    tree.insert(child3_18, "end", text="Prank Biometric Scanners")
    tree.insert(child3_18, "end", text="Screen Pranks")
    tree.insert(child3_18, "end", text="Talking & Answering")
    child3_19 = tree.insert(parent_item3, "end", text="Photo & Video")
    child3_20 = tree.insert(parent_item3, "end", text="Productivity")
    tree.insert(child3_20, "end", text="Alarms & Clocks")
    tree.insert(child3_20, "end", text="Audio Recording")
    tree.insert(child3_20, "end", text="Calculators")
    tree.insert(child3_20, "end", text="Calendars")
    tree.insert(child3_20, "end", text="Cloud Storage")
    tree.insert(child3_20, "end", text="Contact Management")
    tree.insert(child3_20, "end", text="Document Editing")
    tree.insert(child3_20, "end", text="Document Viewers")
    tree.insert(child3_20, "end", text="Email Clients")
    tree.insert(child3_20, "end", text="File Management")
    tree.insert(child3_20, "end", text="Keyboards")
    tree.insert(child3_20, "end", text="Meetings & Conferencing")
    tree.insert(child3_20, "end", text="Notes & Bookmarking")
    tree.insert(child3_20, "end", text="Organizers & Assistants")
    tree.insert(child3_20, "end", text="Personal Finance")
    tree.insert(child3_20, "end", text="Presentations")
    tree.insert(child3_20, "end", text="Remote PC Access")
    tree.insert(child3_20, "end", text="Scanning & Printing")
    tree.insert(child3_20, "end", text="Security")
    tree.insert(child3_20, "end", text="To-Do Lists & Reminders")
    tree.insert(child3_20, "end", text="Translators")
    tree.insert(child3_20, "end", text="Web Browsers")
    child3_21 = tree.insert(parent_item3, "end", text="Reference")
    tree.insert(child3_21, "end", text="Dictionaries")
    tree.insert(child3_21, "end", text="Encyclopedias")
    tree.insert(child3_21, "end", text="Guides & How-Tos")
    tree.insert(child3_21, "end", text="History")
    tree.insert(child3_21, "end", text="Language & Grammar")
    tree.insert(child3_21, "end", text="Math")
    tree.insert(child3_21, "end", text="Reference")
    tree.insert(child3_21, "end", text="Religion")
    tree.insert(child3_21, "end", text="Science")
    tree.insert(child3_21, "end", text="Test Preparation")
    child3_22 = tree.insert(parent_item3, "end", text="Shopping")
    child3_23 = tree.insert(parent_item3, "end", text="Social")
    tree.insert(child3_23, "end", text="Blogging")
    tree.insert(child3_23, "end", text="Dating")
    tree.insert(child3_23, "end", text="Email Clients")
    tree.insert(child3_23, "end", text="General Social Networking")
    tree.insert(child3_23, "end", text="Photo-Sharing")
    tree.insert(child3_23, "end", text="Professional Networking")
    tree.insert(child3_23, "end", text="Social Network Management")
    tree.insert(child3_23, "end", text="Video-Sharing")
    child3_24 = tree.insert(parent_item3, "end", text="Sports")
    tree.insert(child3_24, "end", text="Activity Tracking")
    tree.insert(child3_24, "end", text="Exercise Motivation")
    tree.insert(child3_24, "end", text="Heart Rate Monitors")
    tree.insert(child3_24, "end", text="Sports Fan News")
    tree.insert(child3_24, "end", text="Sports Games")
    tree.insert(child3_24, "end", text="Sports Information")
    tree.insert(child3_24, "end", text="Workout Guides")
    tree.insert(child3_24, "end", text="Yoga Guides")
    child3_25 = tree.insert(parent_item3, "end", text="Transportation")
    tree.insert(child3_25, "end", text="Auto Rental")
    tree.insert(child3_25, "end", text="Flight Finders")
    tree.insert(child3_25, "end", text="Navigation")
    tree.insert(child3_25, "end", text="Taxi & Ridesharing")
    child3_26 = tree.insert(parent_item3, "end", text="Travel")
    tree.insert(child3_26, "end", text="Auto Rental")
    tree.insert(child3_26, "end", text="Compasses")
    tree.insert(child3_26, "end", text="Currency Converters & Guides")
    tree.insert(child3_26, "end", text="Flight Finders")
    tree.insert(child3_26, "end", text="Hotel Finders")
    tree.insert(child3_26, "end", text="Navigation")
    tree.insert(child3_26, "end", text="Offline Maps")
    tree.insert(child3_26, "end", text="Taxi & Ridesharing")
    tree.insert(child3_26, "end", text="Translators")
    tree.insert(child3_26, "end", text="Travel Guides")
    tree.insert(child3_26, "end", text="Trip Planners")
    tree.insert(child3_26, "end", text="Unit Converters")
    child3_27 = tree.insert(parent_item3, "end", text="Utilities")
    tree.insert(child3_27, "end", text="Alarms & Clocks")
    tree.insert(child3_27, "end", text="All-in-One Tools")
    tree.insert(child3_27, "end", text="Audio Recording")
    tree.insert(child3_27, "end", text="Battery Savers")
    tree.insert(child3_27, "end", text="Calculators")
    tree.insert(child3_27, "end", text="Calendars")
    tree.insert(child3_27, "end", text="Cloud Storage")
    tree.insert(child3_27, "end", text="Contact Management")
    tree.insert(child3_27, "end", text="Device Tracking")
    tree.insert(child3_27, "end", text="Document Viewers")
    tree.insert(child3_27, "end", text="Email Clients")
    tree.insert(child3_27, "end", text="File Management")
    tree.insert(child3_27, "end", text="File Transfer")
    tree.insert(child3_27, "end", text="Flashlights")
    tree.insert(child3_27, "end", text="Keyboards")
    tree.insert(child3_27, "end", text="Notes & Bookmarking")
    tree.insert(child3_27, "end", text="QR & Barcode Scanners")
    tree.insert(child3_27, "end", text="Remote PC Access")
    tree.insert(child3_27, "end", text="Scanning & Printing")
    tree.insert(child3_27, "end", text="Security")
    tree.insert(child3_27, "end", text="Speed Testing")
    tree.insert(child3_27, "end", text="Task & App Managers")
    tree.insert(child3_27, "end", text="Translators")
    tree.insert(child3_27, "end", text="Unit Converters")
    tree.insert(child3_27, "end", text="Web Browsers")
    tree.insert(child3_27, "end", text="Wi-Fi Analyzers")
    tree.insert(child3_27, "end", text="Widgets")
    child3_28 = tree.insert(parent_item3, "end", text="Weather")

    parent_item4 = tree.insert("", "end", text="Arts, Crafts & Sewing")
    child4_0 = tree.insert(parent_item4, "end", text="All")

    parent_item5 = tree.insert("", "end", text="Audible Books & Originals")
    child5_0 = tree.insert(parent_item5, "end", text="All")

    parent_item6 = tree.insert("", "end", text="Automotive")
    child6_0 = tree.insert(parent_item6, "end", text="All")

    parent_item7 = tree.insert("", "end", text="Baby")
    child7_0 = tree.insert(parent_item7, "end", text="All")

    parent_item8 = tree.insert("", "end", text="Beauty & Personal Care")
    child8_0 = tree.insert(parent_item8, "end", text="All")

    parent_item9 = tree.insert("", "end", text="Books")
    child9_0 = tree.insert(parent_item9, "end", text="All")

    parent_item3 = tree.insert("", "end", text="Camera & Photo Products")
    child3_0 = tree.insert(parent_item3, "end", text="All")

    parent_item10 = tree.insert("", "end", text="CDs & Vinyl")
    child10_0 = tree.insert(parent_item10, "end", text="All")

    parent_item11 = tree.insert("", "end", text="Cell Phones & Accessories")
    child11_0 = tree.insert(parent_item11, "end", text="Accessories")
    tree.insert(child11_0, "end", text="Adhesive Card Holders", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Adhesive-Card-Holders/zgbs/wireless/21209106011/ref=zg_bs_nav_wireless_2_2407755011')
    child11_0_1 = tree.insert(child11_0, "end", text="Automobile Accessories")
    tree.insert(child11_0_1, "end", text="Automobile Chargers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Automobile-Chargers/zgbs/wireless/2407770011/ref=zg_bs_nav_wireless_3_2407759011')
    tree.insert(child11_0_1, "end", text="Cradles", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Automobile-Cradles/zgbs/wireless/7072562011/ref=zg_bs_nav_wireless_3_2407759011')
    tree.insert(child11_0_1, "end", text="Kits", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Automobile-Accessory-Kits/zgbs/wireless/2407764011/ref=zg_bs_nav_wireless_3_7072562011')
    tree.insert(child11_0_1, "end", text="Pads & Mats", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Automobile-Pads-Mats/zgbs/wireless/11139605011/ref=zg_bs_nav_wireless_3_2407764011')
    tree.insert(child11_0_1, "end", text="Speakerphones", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Automobile-Speakerphones/zgbs/wireless/7073957011/ref=zg_bs_nav_wireless_3_11139605011')
    child11_0_2 = tree.insert(child11_0, "end", text="Cables & Adapters")
    tree.insert(child11_0_2, "end", text="Audio Adapters", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Headphone-Adapters/zgbs/wireless/2267280011/ref=zg_bs_nav_wireless_3_21209107011')
    tree.insert(child11_0_2, "end", text="Lightning Cables", tags='https://www.amazon.com/Best-Sellers-Electronics-Lightning-Cables/zgbs/electronics/6795233011/ref=zg_bs_nav_electronics_4_2267280011')
    tree.insert(child11_0_2, "end", text="OTG Adapters", tags='https://www.amazon.com/Best-Sellers-Electronics-Cell-Phone-OTG-Adapters/zgbs/electronics/21209126011/ref=zg_bs_nav_electronics_4_2267280011')
    tree.insert(child11_0_2, "end", text="USB Cables", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-USB-Cables/zgbs/wireless/464394/ref=zg_bs_nav_wireless_3_21209126011')
    tree.insert(child11_0, "end", text="Camera Privacy Covers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Camera-Privacy-Covers/zgbs/wireless/21103668011/ref=zg_bs_nav_wireless_2_2407755011')
    child11_0_4 = tree.insert(child11_0, "end", text="Chargers & Power Adapters")
    tree.insert(child11_0_4, "end", text="Automobile Chargers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Automobile-Chargers/zgbs/wireless/2407770011/ref=zg_bs_nav_wireless_3_2407761011')
    tree.insert(child11_0_4, "end", text="Battery Charger Cases",tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Battery-Charger-Cases/zgbs/wireless/7073958011/ref=zg_bs_nav_wireless_3_2407770011')
    tree.insert(child11_0_4, "end", text="Charging Stations", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Charging-Stations/zgbs/wireless/12557639011/ref=zg_bs_nav_wireless_3_2407770011')
    tree.insert(child11_0_4, "end", text="Portable Power Banks", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Portable-Power-Banks/zgbs/wireless/7073960011/ref=zg_bs_nav_wireless_3_12557639011')
    tree.insert(child11_0_4, "end", text="Solar Chargers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Solar-Chargers/zgbs/wireless/2407762011/ref=zg_bs_nav_wireless_3_7073960011')
    tree.insert(child11_0_4, "end", text="Wall Chargers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Wall-Chargers/zgbs/wireless/12557637011/ref=zg_bs_nav_wireless_3_2407762011')
    tree.insert(child11_0_4, "end", text="Wireless Chargers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Wireless-Chargers/zgbs/wireless/21209124011/ref=zg_bs_nav_wireless_3_12557637011')
    child11_0_5 = tree.insert(child11_0, "end", text="Décor")
    tree.insert(child11_0_5, "end", text="Home Button Stickers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Home-Button-Stickers/zgbs/wireless/21209119011/ref=zg_bs_nav_wireless_3_21209101011')
    tree.insert(child11_0_5, "end", text="Phone Charms", tags='https://amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Charms/zgbs/wireless/2407779011/ref=zg_bs_nav_wireless_3_21209101011')
    child11_0_6 = tree.insert(child11_0, "end", text="Gaming Accessories")
    tree.insert(child11_0_6, "end", text="Controllers")
    tree.insert(child11_0_6, "end", text="Finger Sleeves")
    tree.insert(child11_0_6, "end", text="Joysticks")
    tree.insert(child11_0_6, "end", text="Screen Expanders & Magnifiers")
    tree.insert(child11_0_6, "end", text="Triggers")
    tree.insert(child11_0_6, "end", text="Virtual Reality (VR) Headsets")
    tree.insert(child11_0, "end", text="Grips", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Grips/zgbs/wireless/21209098011/ref=zg_bs_nav_wireless_2_2407755011')
    child11_0_8 = tree.insert(child11_0, "end", text="Headphones, Earbuds & Accessories")
    tree.insert(child11_0_8, "end", text="Amplifiers", tags='https://www.amazon.com/Best-Sellers-Electronics-Headphone-Amps/zgbs/electronics/13880161/ref=zg_bs_nav_electronics_4_24046923011')
    tree.insert(child11_0_8, "end", text="Audio Adapters", tags='https://www.amazon.com/Best-Sellers-Electronics-Headphone-Adapters/zgbs/electronics/2267280011/ref=zg_bs_nav_electronics_4_13880161')
    tree.insert(child11_0_8, "end", text="Cases", tags='https://www.amazon.com/Best-Sellers-Electronics-Headphone-Cases/zgbs/electronics/2267281011/ref=zg_bs_nav_electronics_4_13880161')
    tree.insert(child11_0_8, "end", text="Earpads", tags='https://www.amazon.com/Best-Sellers-Electronics-Headphone-Earpads/zgbs/electronics/13880181/ref=zg_bs_nav_electronics_4_2267281011')
    tree.insert(child11_0_8, "end", text="Extension Cords", tags='https://www.amazon.com/Best-Sellers-Electronics-Headphone-Extension-Cords/zgbs/electronics/13880171/ref=zg_bs_nav_electronics_4_13880181')
    child11_0_8_1 = tree.insert(child11_0_8, "end", text="Headphones")
    tree.insert(child11_0_8_1, "end", text="Earbud Headphones")
    tree.insert(child11_0_8_1, "end", text="On-Ear Headphones")
    tree.insert(child11_0_8_1, "end", text="Open-Ear Headphones")
    tree.insert(child11_0_8_1, "end", text="Over-Ear Headphones")
    tree.insert(child11_0, "end", text="Item Finders", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Item-Finders/zgbs/wireless/18022313011/ref=zg_bs_nav_wireless_2_2407755011')
    tree.insert(child11_0, "end", text="Lanyards & Wrist Straps", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Lanyards-Wrist-Straps/zgbs/wireless/21209103011/ref=zg_bs_nav_wireless_2_2407755011')
    child11_0_11 = tree.insert(child11_0, "end", text="Maintenance, Upkeep & Repairs")
    tree.insert(child11_0_11, "end", text="Anti-Dust Plugs", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Anti-Dust-Plugs/zgbs/wireless/21209120011/ref=zg_bs_nav_wireless_3_21209105011')
    tree.insert(child11_0_11, "end", text="Home Button Stickers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Home-Button-Stickers/zgbs/wireless/21209119011/ref=zg_bs_nav_wireless_3_21209120011')
    tree.insert(child11_0_11, "end", text="Lens Protectors", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Lens-Protectors/zgbs/wireless/21550399011/ref=zg_bs_nav_wireless_3_21209119011')
    tree.insert(child11_0_11, "end", text="Repair Kits", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Repair-Kits/zgbs/wireless/21209121011/ref=zg_bs_nav_wireless_3_21550399011')
    child11_0_11_0 = tree.insert(child11_0_11, "end", text="Replacement Parts")
    tree.insert(child11_0_11_0, "end", text="Back Covers")
    tree.insert(child11_0_11_0, "end", text="Batteries")
    tree.insert(child11_0_11_0, "end", text="Screens")
    tree.insert(child11_0_11, "end", text="SIM Card Tools & Accessories", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-SIM-Card-Tools-Accessories/zgbs/wireless/14674869011/ref=zg_bs_nav_wireless_3_21209105011')
    tree.insert(child11_0_11, "end", text="Screen Protectors", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Screen-Protectors/zgbs/wireless/2407781011/ref=zg_bs_nav_wireless_3_14674869011')
    tree.insert(child11_0, "end", text="Micro SD Cards", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Micro-SD-Memory-Cards/zgbs/wireless/3015433011/ref=zg_bs_nav_wireless_2_2407755011')
    child11_0_13 = tree.insert(child11_0, "end", text="Mounts")
    tree.insert(child11_0_13, "end", text="Bedstand & Desk Mounts", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Bedstand-Desk-Mounts/zgbs/wireless/23690040011/ref=zg_bs_nav_wireless_3_23690035011')
    tree.insert(child11_0_13, "end", text="Camera Mounts", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Camera-Mounts/zgbs/wireless/23690039011/ref=zg_bs_nav_wireless_3_23690040011')
    tree.insert(child11_0_13, "end", text="Handlebar Mounts", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Handlebar-Mounts/zgbs/wireless/23690037011/ref=zg_bs_nav_wireless_3_23690039011')
    tree.insert(child11_0_13, "end", text="Shower & Wall Mounts", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Shower-Wall-Mounts/zgbs/wireless/23690038011/ref=zg_bs_nav_wireless_3_23690037011')
    child11_0_14 = tree.insert(child11_0, "end", text="Photo & Video Accessories")
    child11_0_14_0 = tree.insert(child11_0_14, "end", text="Flashes & Selfie Lights")
    tree.insert(child11_0_14_0, "end", text="External Flashes", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-External-Flashes/zgbs/wireless/23658830011/ref=zg_bs_nav_wireless_4_18007875011')
    tree.insert(child11_0_14_0, "end", text="Selfie Lights", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Selfie-Lights/zgbs/wireless/23658829011/ref=zg_bs_nav_wireless_4_23658830011')
    tree.insert(child11_0_14, "end", text="Handheld Gimbals & Stabilizers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Handheld-Gimbals-Stabilizers/zgbs/wireless/21209109011/ref=zg_bs_nav_wireless_3_21209100011')
    tree.insert(child11_0_14, "end", text="Lens Attachments", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Lens-Attachments/zgbs/wireless/15124502011/ref=zg_bs_nav_wireless_3_21209109011')
    tree.insert(child11_0_14, "end", text="Photo & Video Kits", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Photo-Video-Kits/zgbs/wireless/21209110011/ref=zg_bs_nav_wireless_3_15124502011')
    tree.insert(child11_0_14, "end", text="Selfie Sticks", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Selfie-Sticks/zgbs/wireless/11139608011/ref=zg_bs_nav_wireless_3_21209110011')
    tree.insert(child11_0_14, "end", text="Tripods", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Tripods/zgbs/wireless/11139610011/ref=zg_bs_nav_wireless_3_11139608011')
    
    child11_0_15 = tree.insert(child11_0, "end", text="Portable Speakers & Docks")
    tree.insert(child11_0_15, "end", text="Audio Docks", tags='https://www.amazon.com/Best-Sellers-Electronics-MP3-Player-Cell-Phone-Audio-Docks/zgbs/electronics/13996491/ref=zg_bs_nav_electronics_3_689637011')
    tree.insert(child11_0_15, "end", text="Portable Bluetooth Speakers", tags='https://www.amazon.com/Best-Sellers-Electronics-Portable-Bluetooth-Speakers/zgbs/electronics/7073956011/ref=zg_bs_nav_electronics_3_13996491')
    tree.insert(child11_0_15, "end", text="Portable Line-In Speakers", tags='https://www.amazon.com/Best-Sellers-Electronics-Portable-Line-In-Speakers/zgbs/electronics/9977446011/ref=zg_bs_nav_electronics_3_7073956011')
    
    tree.insert(child11_0, "end", text="Screen Expanders & Magnifiers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Screen-Expanders-Magnifiers/zgbs/wireless/21209099011/ref=zg_bs_nav_wireless_2_2407755011')
    tree.insert(child11_0, "end", text="Signal Boosters", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Signal-Boosters/zgbs/wireless/2407782011/ref=zg_bs_nav_wireless_2_2407755011')
    tree.insert(child11_0, "end", text="Single Ear Bluetooth Headsets", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Single-Ear-Bluetooth-Cell-Phone-Headsets/zgbs/wireless/18021376011/ref=zg_bs_nav_wireless_2_2407782011')
    child11_0_16 = tree.insert(child11_0, "end", text="Smartwatch Accessories")
    tree.insert(child11_0_16, "end", text="Smartwatch Bands")
    tree.insert(child11_0_16, "end", text="Smartwatch Cables & Chargers")
    tree.insert(child11_0_16, "end", text="Smartwatch Cases")
    tree.insert(child11_0_16, "end", text="Smartwatch Cases with Band")
    tree.insert(child11_0_16, "end", text="Smartwatch Necklaces")
    tree.insert(child11_0_16, "end", text="Smartwatch Screen Protectors")
    tree.insert(child11_0_16, "end", text="Smartwatch Stickers")   
    tree.insert(child11_0, "end", text="Stands", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Stands/zgbs/wireless/23690036011/ref=zg_bs_nav_wireless_2_2407755011')
    tree.insert(child11_0, "end", text="Stylus Pens", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Styluses/zgbs/wireless/11548954011/ref=zg_bs_nav_wireless_2_23690036011')
    tree.insert(child11_0, "end", text="UV Phone Sterilizer Boxes", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-UV-Phone-Sterilizer-Boxes/zgbs/wireless/21268231011/ref=zg_bs_nav_wireless_2_11548954011')
    tree.insert(child11_0, "end", text="Virtual Reality (VR) Headsets", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Virtual-Reality-VR-Headsets/zgbs/wireless/14775002011/ref=zg_bs_nav_wireless_2_21268231011')
       
    child11_1 = tree.insert(parent_item11, "end", text="Cases, Holsters & Clips")
    tree.insert(child11_1, "end", text="Armbands", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Armbands/zgbs/wireless/7073962011/ref=zg_bs_nav_wireless_2_2407760011')
    tree.insert(child11_1, "end", text="Basic Cases", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Basic-Cases/zgbs/wireless/3081461011/ref=zg_bs_nav_wireless_2_7073962011')
    tree.insert(child11_1, "end", text="Battery Charger Cases", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Battery-Charger-Cases/zgbs/wireless/7073958011/ref=zg_bs_nav_wireless_2_3081461011')
    tree.insert(child11_1, "end", text="Bumpers", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Bumpers/zgbs/wireless/17875442011/ref=zg_bs_nav_wireless_2_7073958011')
    tree.insert(child11_1, "end", text="Case & Cover Bundles", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Case-Cover-Bundles/zgbs/wireless/21209096011/ref=zg_bs_nav_wireless_2_17875442011')
    tree.insert(child11_1, "end", text="Crossbody & Lanyard Cases", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Crossbody-Lanyard-Cases/zgbs/wireless/21209095011/ref=zg_bs_nav_wireless_2_21209096011')
    tree.insert(child11_1, "end", text="Dry Bags", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Dry-Bags/zgbs/wireless/17875443011/ref=zg_bs_nav_wireless_2_21209095011')
    tree.insert(child11_1, "end", text="Flip Cases", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Flip-Cell-Phone-Cases/zgbs/wireless/9931389011/ref=zg_bs_nav_wireless_2_17875443011')
    tree.insert(child11_1, "end", text="Holsters", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Holsters/zgbs/wireless/2407765011/ref=zg_bs_nav_wireless_2_9931389011')
    tree.insert(child11_1, "end", text="Sleeves", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-Sleeves/zgbs/wireless/9414313011/ref=zg_bs_nav_wireless_2_2407765011')
    child11_2 = tree.insert(parent_item11, "end", text="SIM Cards & Prepaid Minutes")
    tree.insert(child11_2, "end", text="Cell Phone Minutes", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Prepaid-Cell-Phone-Minutes/zgbs/wireless/2483609011/ref=zg_bs_nav_wireless_2_14674870011')
    tree.insert(child11_2, "end", text="SIM Cards", tags='https://www.amazon.com/Best-Sellers-Cell-Phones-Accessories-Cell-Phone-SIM-Cards/zgbs/wireless/14674870011/ref=zg_bs_nav_wireless_2_2483609011')


    parent_item12 = tree.insert("", "end", text="Climate Pledge Friendly")
    child12_0 = tree.insert(parent_item12, "end", text="All")

    parent_item13 = tree.insert("", "end", text="Clothing, Shoes & Jewelry")
    child13_1 = tree.insert(parent_item13, "end", text="Baby")
    child13_1_0 = tree.insert(child13_1, "end", text="Baby Boys")
    child13_1_0_0 = tree.insert(child13_1_0, "end", text="Accessories")
    child13_1_0_0_0 = tree.insert(child13_1_0_0, "end", text="Bibs & Burp Cloths")
    child13_1_0_0_0_0 = tree.insert(child13_1_0_0_0, "end", text="Bibs")
    tree.insert(child13_1_0_0_0_0, "end", text="Drooling Bibs", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Drooling-Bibs/zgbs/baby-products/21389677011/ref=zg_bs_nav_baby-products_4_7874766011')
    tree.insert(child13_1_0_0_0_0, "end", text="Feeding Bibs", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Feeding-Bibs/zgbs/baby-products/21389675011/ref=zg_bs_nav_baby-products_4_21389677011')
    tree.insert(child13_1_0_0_0_0, "end", text="Teething Bibs", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Teething-Bibs/zgbs/baby-products/21389676011/ref=zg_bs_nav_baby-products_4_21389675011')
    tree.insert(child13_1_0_0_0, "end", text="Bibs & Burp Cloths Sets", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Bibs-Burp-Cloths-Sets/zgbs/baby-products/7874768011/ref=zg_bs_nav_baby-products_3_7874755011')
    tree.insert(child13_1_0_0_0, "end", text="Burp Cloths", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Burp-Cloths/zgbs/baby-products/7874767011/ref=zg_bs_nav_baby-products_3_7874768011')
    tree.insert(child13_1_0_0, "end", text="Gloves & Mittens", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Gloves-Mittens/zgbs/fashion/2478443011/ref=zg_bs_nav_fashion_4_2478436011')
    tree.insert(child13_1_0_0, "end", text="Hats & Caps", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Hats-Caps/zgbs/fashion/2478444011/ref=zg_bs_nav_fashion_4_2478443011')
    tree.insert(child13_1_0_0, "end", text="Leg Warmers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Leg-Warmers/zgbs/fashion/2475843011/ref=zg_bs_nav_fashion_4_2478444011')
    tree.insert(child13_1_0_0, "end", text="Receiving Blankets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Nursery-Receiving-Blankets/zgbs/fashion/302867011/ref=zg_bs_nav_fashion_4_2475843011')
    tree.insert(child13_1_0_0, "end", text="Socks", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Socks/zgbs/fashion/1046202/ref=zg_bs_nav_fashion_4_2475843011')
    child13_1_0_1 = tree.insert(child13_1_0, "end", text="Clothing")
    child13_1_0_1_0 = tree.insert(child13_1_0_1, "end", text="Bloomers, Diaper Covers & Underwear")
    tree.insert(child13_1_0_1_0, "end", text="Bloomers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Bloomers/zgbs/fashion/2237470011/ref=zg_bs_nav_fashion_5_1044522')
    tree.insert(child13_1_0_1_0, "end", text="Training Pants", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Training-Underpants/zgbs/fashion/2475845011/ref=zg_bs_nav_fashion_5_2237470011')
    tree.insert(child13_1_0_1_0, "end", text="Undershirts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Undershirts/zgbs/fashion/2475844011/ref=zg_bs_nav_fashion_5_2475845011')
    tree.insert(child13_1_0_1, "end", text="Bodysuits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Bodysuits/zgbs/fashion/1046184/ref=zg_bs_nav_fashion_4_1044510')
    child13_1_0_1_2 = tree.insert(child13_1_0_1, "end", text="Bottoms")
    tree.insert(child13_1_0_1_2, "end", text="Jeans", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Jeans/zgbs/fashion/2475828011/ref=zg_bs_nav_fashion_5_3526414011')
    tree.insert(child13_1_0_1_2, "end", text="Leggings", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Leggings/zgbs/fashion/10932935011/ref=zg_bs_nav_fashion_5_2475828011')
    tree.insert(child13_1_0_1_2, "end", text="Overalls", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Overalls/zgbs/fashion/1046178/ref=zg_bs_nav_fashion_5_10932935011')
    tree.insert(child13_1_0_1_2, "end", text="Pants", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Pants/zgbs/fashion/1046176/ref=zg_bs_nav_fashion_5_1046178')
    tree.insert(child13_1_0_1_2, "end", text="Shorts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Shorts/zgbs/fashion/1046180/ref=zg_bs_nav_fashion_5_1046176')
    tree.insert(child13_1_0_1, "end", text="Christening", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Christening-Clothing/zgbs/fashion/2475849011/ref=zg_bs_nav_fashion_4_1044510')
    child13_1_0_1_4 = tree.insert(child13_1_0_1, "end", text="Clothing Sets")
    tree.insert(child13_1_0_1_4, "end", text="Pant Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Pants-Sets/zgbs/fashion/6323771011/ref=zg_bs_nav_fashion_5_13698211')
    tree.insert(child13_1_0_1_4, "end", text="Short Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Shorts-Sets/zgbs/fashion/6323772011/ref=zg_bs_nav_fashion_5_6323771011')
    child13_1_0_1_5 = tree.insert(child13_1_0_1, "end", text="Footies & Rompers")
    tree.insert(child13_1_0_1_5, "end", text="Footies", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-One-Piece-Footies/zgbs/fashion/2475848011/ref=zg_bs_nav_fashion_5_3526415011')
    tree.insert(child13_1_0_1_5, "end", text="Rompers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-One-Piece-Rompers/zgbs/fashion/1044520/ref=zg_bs_nav_fashion_5_2475848011')
    tree.insert(child13_1_0_1, "end", text="Hoodies & Active", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Hoodies-Activewear/zgbs/fashion/2475824011/ref=zg_bs_nav_fashion_4_1044510')
    child13_1_0_1_7 = tree.insert(child13_1_0_1, "end", text="Jackets & Coats")
    tree.insert(child13_1_0_1_7, "end", text="Down & Down Alternative", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Down-Coats-Jackets/zgbs/fashion/7132428011/ref=zg_bs_nav_fashion_5_2230685011')
    tree.insert(child13_1_0_1_7, "end", text="Fleece", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Fleece-Outerwear-Jackets/zgbs/fashion/7132427011/ref=zg_bs_nav_fashion_5_7132428011')
    tree.insert(child13_1_0_1_7, "end", text="Jackets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Outerwear-Jackets/zgbs/fashion/2475830011/ref=zg_bs_nav_fashion_5_7132427011')
    tree.insert(child13_1_0_1_7, "end", text="Vests", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Outerwear-Vests/zgbs/fashion/2475831011/ref=zg_bs_nav_fashion_5_2475830011')
    tree.insert(child13_1_0_1, "end", text="Layette Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Layette-Sets/zgbs/fashion/2475852011/ref=zg_bs_nav_fashion_4_1044510')
    child13_1_0_1_9 = tree.insert(child13_1_0_1, "end", text="Sleepwear & Robes")
    tree.insert(child13_1_0_1_9, "end", text="Blanket Sleepers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Blanket-Sleepers/zgbs/fashion/2475840011/ref=zg_bs_nav_fashion_5_2475836011')
    tree.insert(child13_1_0_1_9, "end", text="Nightgowns", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Nightgowns/zgbs/fashion/5088047011/ref=zg_bs_nav_fashion_5_2475840011')
    tree.insert(child13_1_0_1_9, "end", text="Pajama Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Pajama-Sets/zgbs/fashion/2475839011/ref=zg_bs_nav_fashion_5_5088047011')
    tree.insert(child13_1_0_1_9, "end", text="Robes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Robes/zgbs/fashion/2475841011/ref=zg_bs_nav_fashion_5_2475839011')
    child13_1_0_1_10 = tree.insert(child13_1_0_1, "end", text="Snow & Rainwear")
    tree.insert(child13_1_0_1_10, "end", text="Rain Jackets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Raincoats-Jackets/zgbs/fashion/2475833011/ref=zg_bs_nav_fashion_5_82836052011')
    tree.insert(child13_1_0_1_10, "end", text="Snow Pants & Bibs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Snow-Pants-Bibs/zgbs/fashion/2475835011/ref=zg_bs_nav_fashion_5_2475833011')
    tree.insert(child13_1_0_1_10, "end", text="Snow Suits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Snow-Suits/zgbs/fashion/1288638011/ref=zg_bs_nav_fashion_5_2475835011')
    child13_1_0_1_11= tree.insert(child13_1_0_1, "end", text="Suits & Sport Coats")
    tree.insert(child13_1_0_1_11, "end", text="Suits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Suits/zgbs/fashion/2230672011/ref=zg_bs_nav_fashion_5_2475814011')
    tree.insert(child13_1_0_1_11, "end", text="Tuxedos", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Tuxedos/zgbs/fashion/2475816011/ref=zg_bs_nav_fashion_5_2230672011')
    tree.insert(child13_1_0_1, "end", text="Sweaters", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Sweaters/zgbs/fashion/1046188/ref=zg_bs_nav_fashion_4_1044510')
    child13_1_0_1_13 = tree.insert(child13_1_0_1, "end", text="Swim")
    tree.insert(child13_1_0_1_13, "end", text="One Pieces", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-One-Piece-Swimsuits/zgbs/fashion/23709661011/ref=zg_bs_nav_fashion_5_2234613011')
    tree.insert(child13_1_0_1_13, "end", text="Rash Guard Shirts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Rash-Guard-Shirts/zgbs/fashion/2321338011/ref=zg_bs_nav_fashion_5_23709661011')
    tree.insert(child13_1_0_1_13, "end", text="Sunsuits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Swimwear-Sunsuits/zgbs/fashion/6259179011/ref=zg_bs_nav_fashion_5_2321338011')
    tree.insert(child13_1_0_1_13, "end", text="Swim Diapers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Swim-Diapers/zgbs/fashion/2321339011/ref=zg_bs_nav_fashion_5_6259179011')
    child13_1_0_1_13_0 = tree.insert(child13_1_0_1_13, "end", text="Swimwear Sets")
    tree.insert(child13_1_0_1_13_0, "end", text="Cover-Up Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Swimwear-Cover-Up-Sets/zgbs/fashion/6259176011/ref=zg_bs_nav_fashion_6_6259175011')
    tree.insert(child13_1_0_1_13_0, "end", text="Rash Guard Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Rash-Guard-Sets/zgbs/fashion/6259177011/ref=zg_bs_nav_fashion_6_6259176011')
    child13_1_0_1_13_1 = tree.insert(child13_1_0_1_13, "end", text="Trunks & Shorts")
    tree.insert(child13_1_0_1_13_1, "end", text="Board Shorts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Board-Shorts/zgbs/fashion/23709666011/ref=zg_bs_nav_fashion_6_2321340011')
    tree.insert(child13_1_0_1_13_1, "end", text="Trunks", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Swim-Trunks/zgbs/fashion/23709667011/ref=zg_bs_nav_fashion_6_23709666011')
    child13_1_0_1_14= tree.insert(child13_1_0_1, "end", text="Tops")
    tree.insert(child13_1_0_1_14, "end", text="Button-Down & Dress Shirts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Button-Down-Dress-Shirts/zgbs/fashion/2475823011/ref=zg_bs_nav_fashion_5_2475819011')
    tree.insert(child13_1_0_1_14, "end", text="Polos", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Polo-Shirts/zgbs/fashion/2475822011/ref=zg_bs_nav_fashion_5_2475823011')
    tree.insert(child13_1_0_1_14, "end", text="Tees", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Tees/zgbs/fashion/2475820011/ref=zg_bs_nav_fashion_5_2475822011')
    child13_1_0_2 = tree.insert(child13_1_0, "end", text="Shoes")
    tree.insert(child13_1_0_2, "end", text="Athletic & Outdoor", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Athletic-Outdoor-Shoes/zgbs/fashion/8947928011/ref=zg_bs_nav_fashion_4_7239799011')
    tree.insert(child13_1_0_2, "end", text="Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Boots/zgbs/fashion/8947933011/ref=zg_bs_nav_fashion_4_8947928011')
    tree.insert(child13_1_0_2, "end", text="Clogs & Mules", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Clogs-Mules/zgbs/fashion/8947934011/ref=zg_bs_nav_fashion_4_8947933011')
    tree.insert(child13_1_0_2, "end", text="Oxfords & Loafers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Oxfords-Loafers/zgbs/fashion/8947935011/ref=zg_bs_nav_fashion_4_8947934011')
    tree.insert(child13_1_0_2, "end", text="Sandals", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Sandals/zgbs/fashion/8947938011/ref=zg_bs_nav_fashion_4_8947935011')
    tree.insert(child13_1_0_2, "end", text="Slippers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Slippers/zgbs/fashion/8947939011/ref=zg_bs_nav_fashion_4_8947938011')
    tree.insert(child13_1_0_2, "end", text="Sneakers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Boys-Sneakers/zgbs/fashion/8947940011/ref=zg_bs_nav_fashion_4_8947939011')
    child13_1_1 = tree.insert(child13_1, "end", text="Baby Girls")
    child13_1_1_0 = tree.insert(child13_1_1, "end", text="Accessories")
    child13_1_1_0_0 = tree.insert(child13_1_1_0, "end", text="Bibs & Burp Cloths")
    child13_1_1_0_0_0 = tree.insert(child13_1_1_0_0, "end", text="Bibs")
    tree.insert(child13_1_1_0_0_0, "end", text="Drooling Bibs", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Drooling-Bibs/zgbs/baby-products/21389677011/ref=zg_bs_nav_baby-products_4_7874766011')
    tree.insert(child13_1_1_0_0_0, "end", text="Feeding Bibs", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Feeding-Bibs/zgbs/baby-products/21389675011/ref=zg_bs_nav_baby-products_4_21389677011')
    tree.insert(child13_1_1_0_0_0, "end", text="Teething Bibs", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Teething-Bibs/zgbs/baby-products/21389676011/ref=zg_bs_nav_baby-products_4_21389675011')
    tree.insert(child13_1_1_0_0, "end", text="Bibs & Burp Cloths Sets", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Bibs-Burp-Cloths-Sets/zgbs/baby-products/7874768011/ref=zg_bs_nav_baby-products_3_7874755011')
    tree.insert(child13_1_1_0_0, "end", text="Burp Cloths", tags='https://www.amazon.com/Best-Sellers-Baby-Baby-Burp-Cloths/zgbs/baby-products/7874767011/ref=zg_bs_nav_baby-products_3_7874768011')
    tree.insert(child13_1_1_0, "end", text="Gloves & Mittens", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Gloves-Mittens/zgbs/fashion/2478438011/ref=zg_bs_nav_fashion_4_2478435011')
    tree.insert(child13_1_1_0, "end", text="Hats & Caps", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Hats-Caps/zgbs/fashion/2478439011/ref=zg_bs_nav_fashion_4_2478438011')
    tree.insert(child13_1_1_0, "end", text="Headbands", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Headbands/zgbs/fashion/23508741011/ref=zg_bs_nav_fashion_4_2478439011')
    tree.insert(child13_1_1_0, "end", text="Leg Warmers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Leg-Warmers/zgbs/fashion/2475804011/ref=zg_bs_nav_fashion_4_2478439011')
    tree.insert(child13_1_1_0, "end", text="Receiving Blankets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Nursery-Receiving-Blankets/zgbs/fashion/302867011/ref=zg_bs_nav_fashion_4_1258892011')
    tree.insert(child13_1_1_0, "end", text="Socks", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Socks/zgbs/fashion/1258892011/ref=zg_bs_nav_fashion_4_2475804011')
    tree.insert(child13_1_1_0, "end", text="Tights", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Tights/zgbs/fashion/1258893011/ref=zg_bs_nav_fashion_4_1258892011')
    child13_1_1_1 = tree.insert(child13_1_1, "end", text="Clothing")
    child13_1_1_1_0 = tree.insert(child13_1_1_1, "end", text="Bloomers, Diaper Covers & Underwear")
    tree.insert(child13_1_1_1_0, "end", text="Bloomers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Bloomers/zgbs/fashion/2237471011/ref=zg_bs_nav_fashion_5_1044536')
    tree.insert(child13_1_1_1_0, "end", text="Training Pants", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Training-Underpants/zgbs/fashion/2475806011/ref=zg_bs_nav_fashion_5_2237471011')
    tree.insert(child13_1_1_1_0, "end", text="Undershirts, Tanks & Camisoles", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Undershirts/zgbs/fashion/2475805011/ref=zg_bs_nav_fashion_5_2475806011')
    tree.insert(child13_1_1_1, "end", text="Bodysuits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Bodysuits/zgbs/fashion/1046236/ref=zg_bs_nav_fashion_4_1044512')
    child13_1_1_1_2 = tree.insert(child13_1_1_1, "end", text="Bottoms")
    tree.insert(child13_1_1_1_2, "end", text="Jeans", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Jeans/zgbs/fashion/2475788011/ref=zg_bs_nav_fashion_5_3526419011')
    tree.insert(child13_1_1_1_2, "end", text="Leggings", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Leggings/zgbs/fashion/10932934011/ref=zg_bs_nav_fashion_5_2475788011')
    tree.insert(child13_1_1_1_2, "end", text="Overalls", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Overalls/zgbs/fashion/1046222/ref=zg_bs_nav_fashion_5_10932934011')
    tree.insert(child13_1_1_1_2, "end", text="Pants", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Pants/zgbs/fashion/1046220/ref=zg_bs_nav_fashion_5_1046222')
    tree.insert(child13_1_1_1_2, "end", text="Shorts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Shorts/zgbs/fashion/1046224/ref=zg_bs_nav_fashion_5_1046220')
    tree.insert(child13_1_1_1_2, "end", text="Skirts, Skooters & Skorts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Skirts-Skooters-Skorts/zgbs/fashion/1046226/ref=zg_bs_nav_fashion_5_1046224')
    tree.insert(child13_1_1_1, "end", text="Christening", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Christening-Clothing/zgbs/fashion/2475810011/ref=zg_bs_nav_fashion_4_1044512')
    child13_1_1_1_4 = tree.insert(child13_1_1_1, "end", text="Clothing Sets")
    tree.insert(child13_1_1_1_4, "end", text="Pant Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Pant-Sets/zgbs/fashion/6323773011/ref=zg_bs_nav_fashion_5_13697531')
    tree.insert(child13_1_1_1_4, "end", text="Short Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Short-Sets/zgbs/fashion/6323774011/ref=zg_bs_nav_fashion_5_6323773011')
    tree.insert(child13_1_1_1_4, "end", text="Skirt Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Skirt-Sets/zgbs/fashion/6323775011/ref=zg_bs_nav_fashion_5_6323774011')
    child13_1_1_1_6 = tree.insert(child13_1_1_1, "end", text="Dresses")
    tree.insert(child13_1_1_1_6, "end", text="Playwear", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Playwear-Dresses/zgbs/fashion/2475776011/ref=zg_bs_nav_fashion_5_1044542')
    tree.insert(child13_1_1_1_6, "end", text="Special Occasion", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Special-Occasion-Dresses/zgbs/fashion/2475775011/ref=zg_bs_nav_fashion_5_2475776011')     
    child13_1_1_1_5 = tree.insert(child13_1_1_1, "end", text="Footies & Rompers")
    tree.insert(child13_1_1_1_5, "end", text="Footies", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-One-Piece-Footies/zgbs/fashion/2475809011/ref=zg_bs_nav_fashion_5_3526420011')
    tree.insert(child13_1_1_1_5, "end", text="Rompers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-One-Piece-Rompers/zgbs/fashion/699905011/ref=zg_bs_nav_fashion_5_2475809011')
    tree.insert(child13_1_1_1, "end", text="Hoodies & Active", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Hoodies-Activewear/zgbs/fashion/2475784011/ref=zg_bs_nav_fashion_4_1044512')
    child13_1_1_1_7 = tree.insert(child13_1_1_1, "end", text="Jackets & Coats")
    tree.insert(child13_1_1_1_7, "end", text="Down & Down Alternative", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Down-Jackets-Coats/zgbs/fashion/7132415011/ref=zg_bs_nav_fashion_5_2230684011')
    tree.insert(child13_1_1_1_7, "end", text="Fleece", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Fleece-Jackets-Coats/zgbs/fashion/7132414011/ref=zg_bs_nav_fashion_5_7132415011')
    tree.insert(child13_1_1_1_7, "end", text="Jackets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Outerwear-Jackets/zgbs/fashion/2475790011/ref=zg_bs_nav_fashion_5_7132414011')
    tree.insert(child13_1_1_1_7, "end", text="Vests", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Outerwear-Vests/zgbs/fashion/2475791011/ref=zg_bs_nav_fashion_5_2475790011')
    tree.insert(child13_1_1_1, "end", text="Layette Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Layette-Sets/zgbs/fashion/2475813011/ref=zg_bs_nav_fashion_4_1044512')
    child13_1_1_1_9 = tree.insert(child13_1_1_1, "end", text="Sleepwear & Robes")
    tree.insert(child13_1_1_1_9, "end", text="Blanket Sleepers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Blanket-Sleepers/zgbs/fashion/2475800011/ref=zg_bs_nav_fashion_5_2475796011')
    tree.insert(child13_1_1_1_9, "end", text="Nightgowns", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Nightgowns/zgbs/fashion/2475801011/ref=zg_bs_nav_fashion_5_2475800011')
    tree.insert(child13_1_1_1_9, "end", text="Pajama Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Pajama-Sets/zgbs/fashion/2475799011/ref=zg_bs_nav_fashion_5_2475801011')
    tree.insert(child13_1_1_1_9, "end", text="Robes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Robes/zgbs/fashion/2475802011/ref=zg_bs_nav_fashion_5_2475799011')
    child13_1_1_1_10 = tree.insert(child13_1_1_1, "end", text="Snow & Rainwear")
    tree.insert(child13_1_1_1_10, "end", text="Rain Jackets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Raincoats-Jackets/zgbs/fashion/2475793011/ref=zg_bs_nav_fashion_5_82836051011')
    tree.insert(child13_1_1_1_10, "end", text="Snow Pants & Bibs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Snow-Pants-Bibs/zgbs/fashion/2475795011/ref=zg_bs_nav_fashion_5_2475793011')
    tree.insert(child13_1_1_1_10, "end", text="Snow Suits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Snow-Suits/zgbs/fashion/1288639011/ref=zg_bs_nav_fashion_5_2475795011')
    tree.insert(child13_1_1_1, "end", text="Sweaters", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Sweaters/zgbs/fashion/1046240/ref=zg_bs_nav_fashion_4_1044512')
    child13_1_1_1_13 = tree.insert(child13_1_1_1, "end", text="Swim")
    tree.insert(child13_1_1_1_13, "end", text="Board Shorts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Board-Shorts/zgbs/fashion/23709660011/ref=zg_bs_nav_fashion_5_2234612011')
    tree.insert(child13_1_1_1_13, "end", text="Cover-Ups", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Swimwear-Cover-Ups/zgbs/fashion/2321331011/ref=zg_bs_nav_fashion_5_23709660011')
    tree.insert(child13_1_1_1_13, "end", text="One Pieces", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-One-Piece-Swimsuits/zgbs/fashion/2321328011/ref=zg_bs_nav_fashion_5_2321331011')
    tree.insert(child13_1_1_1_13, "end", text="Rash Guard Shirts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Rash-Guard-Shirts/zgbs/fashion/2321330011/ref=zg_bs_nav_fashion_5_2321328011')
    tree.insert(child13_1_1_1_13, "end", text="Sunsuits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Swimwear-Sunsuits/zgbs/fashion/6259184011/ref=zg_bs_nav_fashion_5_2321330011')
    tree.insert(child13_1_1_1_13, "end", text="Swim Diapers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Swim-Diapers/zgbs/fashion/2321332011/ref=zg_bs_nav_fashion_5_6259184011')
    child13_1_1_1_13_0 = tree.insert(child13_1_1_1_13, "end", text="Swimwear Sets")
    tree.insert(child13_1_1_1_13_0, "end", text="Cover-Up Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Swimwear-Cover-Up-Sets/zgbs/fashion/6259182011/ref=zg_bs_nav_fashion_6_23771259011')
    tree.insert(child13_1_1_1_13_0, "end", text="Rash Guard Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Rash-Guard-Sets/zgbs/fashion/6259183011/ref=zg_bs_nav_fashion_6_6259182011')
    child13_1_1_1_13_1 = tree.insert(child13_1_1_1_13, "end", text="Two-Pieces")
    tree.insert(child13_1_1_1_13_1, "end", text="Bikinis", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Bikini-Sets/zgbs/fashion/6259181011/ref=zg_bs_nav_fashion_6_2321329011')
    tree.insert(child13_1_1_1_13_1, "end", text="Tankinis", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Tankini-Sets/zgbs/fashion/6259180011/ref=zg_bs_nav_fashion_6_6259181011')
    child13_1_1_1_14= tree.insert(child13_1_1_1, "end", text="Tops")
    tree.insert(child13_1_1_1_14, "end", text="Blouses", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Blouses/zgbs/fashion/2475782011/ref=zg_bs_nav_fashion_5_1044532')
    tree.insert(child13_1_1_1_14, "end", text="Tank Tops", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Tank-Tops/zgbs/fashion/5088048011/ref=zg_bs_nav_fashion_5_2475782011')
    tree.insert(child13_1_1_1_14, "end", text="Tees", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Tees/zgbs/fashion/2475780011/ref=zg_bs_nav_fashion_5_5088048011')
    child13_1_1_2 = tree.insert(child13_1_1, "end", text="Shoes")
    tree.insert(child13_1_1_2, "end", text="Athletic & Outdoor", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Athletic-Outdoor-Shoes/zgbs/fashion/8947910011/ref=zg_bs_nav_fashion_4_7239798011')
    tree.insert(child13_1_1_2, "end", text="Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Boots/zgbs/fashion/8947917011/ref=zg_bs_nav_fashion_4_8947910011')
    tree.insert(child13_1_1_2, "end", text="Clogs & Mules", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Clogs-Mules/zgbs/fashion/8947918011/ref=zg_bs_nav_fashion_4_8947917011')
    child13_1_1_2_0 = tree.insert(child13_1_1_2, "end", text="Flats")
    tree.insert(child13_1_1_2_0, "end", text="Ballet", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Ballet-Flats/zgbs/fashion/8947920011/ref=zg_bs_nav_fashion_5_8947919011')
    tree.insert(child13_1_1_2_0, "end", text="Mary Jane", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Mary-Jane-Flats/zgbs/fashion/8947921011/ref=zg_bs_nav_fashion_5_8947920011')
    tree.insert(child13_1_1_2_0, "end", text="Oxford & Loafer", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Oxford-Loafer-Flats/zgbs/fashion/8947922011/ref=zg_bs_nav_fashion_5_8947921011')
    tree.insert(child13_1_1_2, "end", text="Sandals", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Sandals/zgbs/fashion/8947925011/ref=zg_bs_nav_fashion_4_7239798011')
    tree.insert(child13_1_1_2, "end", text="Slippers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Slippers/zgbs/fashion/8947926011/ref=zg_bs_nav_fashion_4_8947925011')
    tree.insert(child13_1_1_2, "end", text="Sneakers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Baby-Girls-Sneakers/zgbs/fashion/8947927011/ref=zg_bs_nav_fashion_4_8947926011')
    
    
    child13_2 = tree.insert(parent_item13, "end", text="Boys")
    child13_2_0 = tree.insert(child13_2, "end", text="All")
    child13_3 = tree.insert(parent_item13, "end", text="Costumes & Accessories")
    child13_3_0 = tree.insert(child13_3, "end", text="All")
    child13_3_1 = tree.insert(child13_3, "end", text="Kids & Baby")
    child13_3_1_0 = tree.insert(child13_3_1, "end", text="All", tags='https://www.amazon.com/RFID-Blocking-Slim-Wallet-Moneyclip-Metal-Wallet/dp/B097G9HJTK?th=1')    
    child13_3_1_1 = tree.insert(child13_3_1, "end", text="Baby")    
    child13_3_1_2 = tree.insert(child13_3_1, "end", text="Boys")    
    child13_3_1_3 = tree.insert(child13_3_1, "end", text="Girls")    
    child13_3_2 = tree.insert(child13_3, "end", text="Makeup, Facial Hair & Adhesives")
    child13_3_2_0 = tree.insert(child13_3_2, "end", text="All")    
    child13_3_3 = tree.insert(child13_3, "end", text="Men")
    child13_3_3_0 = tree.insert(child13_3_3, "end", text="All")    
    child13_3_4 = tree.insert(child13_3, "end", text="Props")
    child13_3_4_0 = tree.insert(child13_3_4, "end", text="All")    
    child13_3_5 = tree.insert(child13_3, "end", text="Women")
    child13_3_5_0 = tree.insert(child13_3_5, "end", text="All")    
    child13_4 = tree.insert(parent_item13, "end", text="Girls")
    child13_4_0 = tree.insert(child13_4, "end", text="All")
    child13_5 = tree.insert(parent_item13, "end", text="Luggage & Travel Gear")
    child13_5_0 = tree.insert(child13_5, "end", text="All")
    child13_6 = tree.insert(parent_item13, "end", text="Men")
    child13_6_1 = tree.insert(child13_6, "end", text="Accessories")
    tree.insert(child13_6_1, "end", text="Belts", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Belts/zgbs/fashion/2474947011/ref=zg_bs_nav_fashion_3_11002536011')
    tree.insert(child13_6_1, "end", text="Collar Stays", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Collar-Stays/zgbs/fashion/11002536011/ref=zg_bs_nav_fashion_3_2474937011')
    child13_6_1_3 = tree.insert(child13_6_1, "end", text="Cuff Links, Shirt Studs & Tie Clips")
    tree.insert(child13_6_1_3, "end", text="Cuff Links", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cuff-Links/zgbs/fashion/3888131/ref=zg_bs_nav_fashion_4_7072329011')
    tree.insert(child13_6_1_3, "end", text="Shirt Studs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shirt-Studs/zgbs/fashion/3888381/ref=zg_bs_nav_fashion_4_7072329011')
    tree.insert(child13_6_1_3, "end", text="Tie Clips", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Tie-Clips/zgbs/fashion/3888391/ref=zg_bs_nav_fashion_4_7072329011')
    tree.insert(child13_6_1, "end", text="Earmuffs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Earmuffs/zgbs/fashion/2474986011/ref=zg_bs_nav_fashion_3_2474937011')
    child13_6_1_5 = tree.insert(child13_6_1, "end", text="Gloves & Mittens")
    tree.insert(child13_6_1_5, "end", text="Cold Weather Gloves", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cold-Weather-Gloves/zgbs/fashion/2474987011/ref=zg_bs_nav_fashion_4_7072331011')
    tree.insert(child13_6_1_5, "end", text="Mittens", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cold-Weather-Mittens/zgbs/fashion/2478146011/ref=zg_bs_nav_fashion_4_2474987011')
    tree.insert(child13_6_1, "end", text="Hand Fans", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Hand-Fans/zgbs/fashion/21224652011/ref=zg_bs_nav_fashion_3_2474953011')
    tree.insert(child13_6_1, "end", text="Handkerchiefs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Handkerchiefs/zgbs/fashion/2474953011/ref=zg_bs_nav_fashion_3_2475889011')
    child13_6_1_8 = tree.insert(child13_6_1, "end", text="Hats & Caps")
    tree.insert(child13_6_1_8, "end", text="Balaclavas", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Balaclavas/zgbs/fashion/2474985011/ref=zg_bs_nav_fashion_4_2474996011')
    tree.insert(child13_6_1_8, "end", text="Baseball Caps", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Baseball-Caps/zgbs/fashion/2474996011/ref=zg_bs_nav_fashion_4_2474985011')
    tree.insert(child13_6_1_8, "end", text="Bomber Hats", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Bomber-Hats/zgbs/fashion/7240237011/ref=zg_bs_nav_fashion_4_2474996011')
    tree.insert(child13_6_1_8, "end", text="Cowboy Hats", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cowboy-Hats/zgbs/fashion/2474998011/ref=zg_bs_nav_fashion_4_7240237011')
    tree.insert(child13_6_1_8, "end", text="Fedoras", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Fedoras/zgbs/fashion/2474999011/ref=zg_bs_nav_fashion_4_2474998011')
    tree.insert(child13_6_1_8, "end", text="Newsboy Caps", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Newsboy-Caps/zgbs/fashion/2475002011/ref=zg_bs_nav_fashion_4_2474999011')
    tree.insert(child13_6_1_8, "end", text="Rain Hats", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Rain-Hats/zgbs/fashion/2578667011/ref=zg_bs_nav_fashion_4_2475002011')
    tree.insert(child13_6_1_8, "end", text="Skullies & Beanies", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Skullies-Beanies/zgbs/fashion/2475004011/ref=zg_bs_nav_fashion_4_2578667011')
    tree.insert(child13_6_1_8, "end", text="Sun Hats", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Sun-Hats/zgbs/fashion/2578668011/ref=zg_bs_nav_fashion_4_2475004011')
    tree.insert(child13_6_1_8, "end", text="Visors", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Visors/zgbs/fashion/2475005011/ref=zg_bs_nav_fashion_4_2578668011')
    tree.insert(child13_6_1, "end", text="Keyrings & Keychains", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Keyrings-Keychains/zgbs/fashion/2475889011/ref=zg_bs_nav_fashion_3_2474937011')
    child13_6_1_10 = tree.insert(child13_6_1, "end", text="Scarves")
    tree.insert(child13_6_1_10, "end", text="Cold Weather Scarves", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cold-Weather-Scarves/zgbs/fashion/2474990011/ref=zg_bs_nav_fashion_4_7072332011')
    tree.insert(child13_6_1_10, "end", text="Fashion Scarves", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Fashion-Scarves/zgbs/fashion/2474952011/ref=zg_bs_nav_fashion_4_2474990011')
    tree.insert(child13_6_1_10, "end", text="Neck Gaiters", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cold-Weather-Neck-Gaiters/zgbs/fashion/2578666011/ref=zg_bs_nav_fashion_4_7072332011')
    child13_6_1_11 = tree.insert(child13_6_1, "end", text="Sport Headbands", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Sport-Headbands/zgbs/fashion/23466428011/ref=zg_bs_nav_fashion_3_2474937011')
    child13_6_1_12 = tree.insert(child13_6_1, "end", text="Sunglasses & Eyewear Accessories")
    tree.insert(child13_6_1_12, "end", text="Eyeglass Cases", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Eyeglass-Cases/zgbs/fashion/3478924011/ref=zg_bs_nav_fashion_4_7072330011')
    tree.insert(child13_6_1_12, "end", text="Eyeglass Chains", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Eyeglass-Chains/zgbs/fashion/3478926011/ref=zg_bs_nav_fashion_4_3478924011')
    tree.insert(child13_6_1_12, "end", text="Eyewear Frames", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Eyewear-Frames/zgbs/fashion/3478922011/ref=zg_bs_nav_fashion_4_3478926011')
    tree.insert(child13_6_1_12, "end", text="Replacement Sunglass Lenses", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Replacement-Sunglass-Lenses/zgbs/fashion/3508163011/ref=zg_bs_nav_fashion_4_3478922011')
    tree.insert(child13_6_1_12, "end", text="Sunglasses", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Sunglasses/zgbs/fashion/2474995011/ref=zg_bs_nav_fashion_4_3508163011')
    tree.insert(child13_6_1, "end", text="Suspenders", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Suspenders/zgbs/fashion/2474956011/ref=zg_bs_nav_fashion_3_2474937011')
    child13_6_1_14 = tree.insert(child13_6_1, "end", text="Ties, Cummerbunds & Pocket Squares")
    tree.insert(child13_6_1_14, "end", text="Bolo Ties", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Bolo-Ties/zgbs/fashion/17874825011/ref=zg_bs_nav_fashion_4_17874824011')
    tree.insert(child13_6_1_14, "end", text="Bow Ties", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Bow-Ties/zgbs/fashion/2474948011/ref=zg_bs_nav_fashion_4_17874826011')
    tree.insert(child13_6_1_14, "end", text="Cravats", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cravats/zgbs/fashion/17874826011/ref=zg_bs_nav_fashion_4_2474948011')
    tree.insert(child13_6_1_14, "end", text="Cummerbunds", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cummerbunds/zgbs/fashion/2474950011/ref=zg_bs_nav_fashion_4_17874826011')
    tree.insert(child13_6_1_14, "end", text="Neckties", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Neckties/zgbs/fashion/2474955011/ref=zg_bs_nav_fashion_4_2474950011')
    tree.insert(child13_6_1_14, "end", text="Pocket Squares", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Pocket-Squares/zgbs/fashion/17874828011/ref=zg_bs_nav_fashion_4_2474955011')
    tree.insert(child13_6_1_14, "end", text="Tie Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Tie-Sets/zgbs/fashion/17874830011/ref=zg_bs_nav_fashion_4_17874828011')
    child13_6_1_15 = tree.insert(child13_6_1, "end", text="Wallets, Card Cases & Money Organizers")
    child13_6_1_15_0 = tree.insert(child13_6_1_15, "end", text="Card & ID Cases") 
    tree.insert(child13_6_1_15_0, "end", text="Business Card Cases", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Business-Card-Cases/zgbs/fashion/3420362011/ref=zg_bs_nav_fashion_5_2503687011')   
    tree.insert(child13_6_1_15_0, "end", text="Card Cases", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Card-Cases/zgbs/fashion/2503686011/ref=zg_bs_nav_fashion_5_3420362011')   
    tree.insert(child13_6_1_15_0, "end", text="Commuter Pass Cases", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Commuter-Pass-Cases/zgbs/fashion/3420363011/ref=zg_bs_nav_fashion_5_2503686011')   
    tree.insert(child13_6_1_15_0, "end", text="ID Cases", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-ID-Cases/zgbs/fashion/2503687011/ref=zg_bs_nav_fashion_5_3420363011')   
    tree.insert(child13_6_1_15, "end", text="Coin Purses & Pouches", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Coin-Purses-Pouches/zgbs/fashion/2475888011/ref=zg_bs_nav_fashion_4_2475894011')    
    tree.insert(child13_6_1_15, "end", text="Money Clips", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Money-Clips/zgbs/fashion/2475894011/ref=zg_bs_nav_fashion_4_2475895011')    
    tree.insert(child13_6_1_15, "end", text="Wallets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Wallets/zgbs/fashion/2475895011/ref=zg_bs_nav_fashion_4_7072333011')    
    child13_6_2 = tree.insert(child13_6, "end", text="Clothing")
    child13_6_2_0 = tree.insert(child13_6_2, "end", text="All")    
    child13_6_3 = tree.insert(child13_6, "end", text="Handbags & Shoulder Bags")
    child13_6_3_0 = tree.insert(child13_6_3, "end", text="Cross-Body Sling Bags", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cross-Body-Sling-Bags/zgbs/fashion/21557335011/ref=zg_bs_nav_fashion_3_14864589011')    
    child13_6_3_1 = tree.insert(child13_6_3, "end", text="Shoulder Bags", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Shoulder-Bags/zgbs/fashion/21557338011/ref=zg_bs_nav_fashion_3_21557335011')    
    child13_6_3_2 = tree.insert(child13_6_3, "end", text="Top-Handle Bags", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Top-Handle-Bags/zgbs/fashion/21557337011/ref=zg_bs_nav_fashion_3_21557338011')    
    child13_6_3_3 = tree.insert(child13_6_3, "end", text="Totes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Totes/zgbs/fashion/21557336011/ref=zg_bs_nav_fashion_3_21557337011')    
    child13_6_4 = tree.insert(child13_6, "end", text="Jewelry")
    child13_6_4_0 = tree.insert(child13_6_4, "end", text="Body Jewelry")    
    tree.insert(child13_6_4_0, "end", text="Dental Grills", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Dental-Grills/zgbs/fashion/17880337011/ref=zg_bs_nav_fashion_4_17880327011')    
    tree.insert(child13_6_4_0, "end", text="Faux Body Piercing Jewelry", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Faux-Body-Piercing-Jewelry/zgbs/fashion/17880338011/ref=zg_bs_nav_fashion_4_17880337011')    
    child13_6_4_0_0 = tree.insert(child13_6_4_0, "end", text="Piercing Jewelry")    
    tree.insert(child13_6_4_0_0, "end", text="Barbells", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Body-Piercing-Barbells/zgbs/fashion/17880329011/ref=zg_bs_nav_fashion_5_17880328011') 
    tree.insert(child13_6_4_0_0, "end", text="Plugs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Body-Piercing-Plugs/zgbs/fashion/17880330011/ref=zg_bs_nav_fashion_5_17880329011') 
    tree.insert(child13_6_4_0_0, "end", text="Retainers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Body-Piercing-Retainers/zgbs/fashion/17880331011/ref=zg_bs_nav_fashion_5_17880330011') 
    tree.insert(child13_6_4_0_0, "end", text="Rings", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Body-Piercing-Rings/zgbs/fashion/17880332011/ref=zg_bs_nav_fashion_5_17880331011') 
    tree.insert(child13_6_4_0_0, "end", text="Screws", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Body-Piercing-Screws/zgbs/fashion/17880333011/ref=zg_bs_nav_fashion_5_17880332011') 
    tree.insert(child13_6_4_0_0, "end", text="Studs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Body-Piercing-Studs/zgbs/fashion/17880334011/ref=zg_bs_nav_fashion_5_17880333011') 
    tree.insert(child13_6_4_0_0, "end", text="Tapers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Body-Piercing-Tapers/zgbs/fashion/17880335011/ref=zg_bs_nav_fashion_5_17880334011') 
    tree.insert(child13_6_4_0_0, "end", text="Tunnels", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Body-Piercing-Tunnels/zgbs/fashion/17880336011/ref=zg_bs_nav_fashion_5_17880335011') 
    tree.insert(child13_6_4_0, "end", text="Toe Rings", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Toe-Rings/zgbs/fashion/17880339011/ref=zg_bs_nav_fashion_4_17880327011')    
    child13_6_4_1 = tree.insert(child13_6_4, "end", text="Bracelets")   
    tree.insert(child13_6_4_1, "end", text="Cuff", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cuff-Bracelets/zgbs/fashion/3888091/ref=zg_bs_nav_fashion_4_3888081')  
    tree.insert(child13_6_4_1, "end", text="Identification", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-ID-Bracelets/zgbs/fashion/3888101/ref=zg_bs_nav_fashion_4_3888091')  
    tree.insert(child13_6_4_1, "end", text="Link", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Link-Bracelets/zgbs/fashion/3888111/ref=zg_bs_nav_fashion_4_3888101')   
    tree.insert(child13_6_4, "end", text="Cuff Links", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cuff-Links/zgbs/fashion/3888131/ref=zg_bs_nav_fashion_3_3887881')    
    tree.insert(child13_6_4, "end", text="Earrings", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Earrings/zgbs/fashion/3888141/ref=zg_bs_nav_fashion_3_3888131')    
    tree.insert(child13_6_4, "end", text="Necklaces", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Necklaces/zgbs/fashion/3888121/ref=zg_bs_nav_fashion_3_3888141')    
    tree.insert(child13_6_4, "end", text="Pendants", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Pendants/zgbs/fashion/21550946011/ref=zg_bs_nav_fashion_3_3888121')    
    tree.insert(child13_6_4, "end", text="Rings", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Rings/zgbs/fashion/3888171/ref=zg_bs_nav_fashion_3_21550946011')    
    tree.insert(child13_6_4, "end", text="Shirt Studs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shirt-Studs/zgbs/fashion/3888381/ref=zg_bs_nav_fashion_3_3888171')    
    tree.insert(child13_6_4, "end", text="Tie Clips", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Tie-Clips/zgbs/fashion/3888391/ref=zg_bs_nav_fashion_3_3888381')    
    tree.insert(child13_6_4, "end", text="Tie Pins", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Tie-Pins/zgbs/fashion/3888411/ref=zg_bs_nav_fashion_3_3888391')    
    tree.insert(child13_6_4, "end", text="Wedding Rings", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Wedding-Rings/zgbs/fashion/9539904011/ref=zg_bs_nav_fashion_3_3888411')    
    child13_6_5 = tree.insert(child13_6, "end", text="Shoes")
    child13_6_5_0 = tree.insert(child13_6_5, "end", text="Athletic")   
    tree.insert(child13_6_5_0, "end", text="Ballet & Dance", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Dance-Shoes/zgbs/fashion/679273011/ref=zg_bs_nav_fashion_4_6127770011') 
    tree.insert(child13_6_5_0, "end", text="Bowling", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Bowling-Shoes/zgbs/fashion/679268011/ref=zg_bs_nav_fashion_4_679273011') 
    tree.insert(child13_6_5_0, "end", text="Cycling", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cycling-Shoes/zgbs/fashion/679272011/ref=zg_bs_nav_fashion_4_679268011') 
    tree.insert(child13_6_5_0, "end", text="Equestrian Sport Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Equestrian-Sport-Boots/zgbs/fashion/3420978011/ref=zg_bs_nav_fashion_4_679272011') 
    tree.insert(child13_6_5_0, "end", text="Fitness & Cross-Training", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Cross-Training-Shoes/zgbs/fashion/679271011/ref=zg_bs_nav_fashion_4_3420978011') 
    tree.insert(child13_6_5_0, "end", text="Golf", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Golf-Shoes/zgbs/fashion/679278011/ref=zg_bs_nav_fashion_4_679271011') 
    child13_6_5_0_0 = tree.insert(child13_6_5_0, "end", text="Running") 
    tree.insert(child13_6_5_0_0, "end", text="Road Running", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Road-Running-Shoes/zgbs/fashion/14210389011/ref=zg_bs_nav_fashion_5_679286011') 
    tree.insert(child13_6_5_0_0, "end", text="Track & Field & Cross Country", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Track-Field-Cross-Country-Shoes/zgbs/fashion/3420973011/ref=zg_bs_nav_fashion_5_14210389011') 
    tree.insert(child13_6_5_0_0, "end", text="Trail Running", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Trail-Running-Shoes/zgbs/fashion/1264575011/ref=zg_bs_nav_fashion_5_3420973011') 
    tree.insert(child13_6_5_0, "end", text="Skateboarding", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Skateboarding-Shoes/zgbs/fashion/679295011/ref=zg_bs_nav_fashion_4_6127770011') 
    tree.insert(child13_6_5_0, "end", text="Sport Sandals & Slides", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Athletic-Outdoor-Sandals-Slides/zgbs/fashion/679291011/ref=zg_bs_nav_fashion_4_679295011') 
    child13_6_5_0_1 = tree.insert(child13_6_5_0, "end", text="Team Sports") 
    tree.insert(child13_6_5_0_1, "end", text="Baseball & Softball", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Baseball-Softball-Shoes/zgbs/fashion/679257011/ref=zg_bs_nav_fashion_5_10294506011') 
    tree.insert(child13_6_5_0_1, "end", text="Basketball", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Basketball-Shoes/zgbs/fashion/679260011/ref=zg_bs_nav_fashion_5_679257011') 
    tree.insert(child13_6_5_0_1, "end", text="Field Hockey & Lacrosse", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Field-Hockey-Lacrosse-Shoes/zgbs/fashion/3420960011/ref=zg_bs_nav_fashion_5_679260011') 
    tree.insert(child13_6_5_0_1, "end", text="Football", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Football-Shoes/zgbs/fashion/679275011/ref=zg_bs_nav_fashion_5_3420960011') 
    tree.insert(child13_6_5_0_1, "end", text="Rugby", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Rugby-Shoes/zgbs/fashion/683179011/ref=zg_bs_nav_fashion_5_679275011') 
    tree.insert(child13_6_5_0_1, "end", text="Soccer", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Soccer-Shoes/zgbs/fashion/679296011/ref=zg_bs_nav_fashion_5_683179011') 
    tree.insert(child13_6_5_0_1, "end", text="Volleyball", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Volleyball-Shoes/zgbs/fashion/679302011/ref=zg_bs_nav_fashion_5_679296011') 
    tree.insert(child13_6_5_0, "end", text="Tennis & Racquet Sports", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Tennis-Racquet-Sport-Shoes/zgbs/fashion/3420963011/ref=zg_bs_nav_fashion_4_6127770011') 
    tree.insert(child13_6_5_0, "end", text="Walking", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Walking-Shoes/zgbs/fashion/679303011/ref=zg_bs_nav_fashion_4_3420963011') 
    tree.insert(child13_6_5_0, "end", text="Water Shoes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Water-Shoes/zgbs/fashion/679304011/ref=zg_bs_nav_fashion_4_679303011') 
    tree.insert(child13_6_5_0, "end", text="Wrestling", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Wrestling-Shoes/zgbs/fashion/679305011/ref=zg_bs_nav_fashion_4_679304011') 
    child13_6_5_1 = tree.insert(child13_6_5, "end", text="Boots")    
    tree.insert(child13_6_5_1, "end", text="Chelsea", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Chelsea-Boots/zgbs/fashion/11721157011/ref=zg_bs_nav_fashion_4_679307011')    
    tree.insert(child13_6_5_1, "end", text="Chukka", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Chukka-Boots/zgbs/fashion/11721158011/ref=zg_bs_nav_fashion_4_11721157011')    
    tree.insert(child13_6_5_1, "end", text="Hiking Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Hiking-Boots/zgbs/fashion/679280011/ref=zg_bs_nav_fashion_4_11721158011')    
    tree.insert(child13_6_5_1, "end", text="Hunting", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Hunting-Shoes/zgbs/fashion/679283011/ref=zg_bs_nav_fashion_4_11721158011')    
    tree.insert(child13_6_5_1, "end", text="Motorcycle & Combat", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Motorcycle-Combat-Boots/zgbs/fashion/11721160011/ref=zg_bs_nav_fashion_4_11721158011')    
    tree.insert(child13_6_5_1, "end", text="Oxford & Derby", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Oxford-Derby-Boots/zgbs/fashion/11721163011/ref=zg_bs_nav_fashion_4_11721160011')    
    tree.insert(child13_6_5_1, "end", text="Rain", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Rain-Boots/zgbs/fashion/679266011/ref=zg_bs_nav_fashion_4_11721163011')    
    tree.insert(child13_6_5_1, "end", text="Snow Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Snow-Boots/zgbs/fashion/5658904011/ref=zg_bs_nav_fashion_4_679266011')    
    tree.insert(child13_6_5_1, "end", text="Western", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Western-Boots/zgbs/fashion/11721159011/ref=zg_bs_nav_fashion_4_679266011')    
    child13_6_5_1_9 = tree.insert(child13_6_5_1, "end", text="Work & Safety")   
    tree.insert(child13_6_5_1_9, "end", text="Fire & Safety Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Fire-Safety-Boots/zgbs/fashion/11751043011/ref=zg_bs_nav_fashion_5_11721164011') 
    tree.insert(child13_6_5_1_9, "end", text="Industrial & Construction Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Industrial-Construction-Boots/zgbs/fashion/11751044011/ref=zg_bs_nav_fashion_5_11751043011') 
    tree.insert(child13_6_5_1_9, "end", text="Military & Tactical", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Military-Tactical-Boots/zgbs/fashion/6796862011/ref=zg_bs_nav_fashion_5_11751043011')  
    child13_6_5_2 = tree.insert(child13_6_5, "end", text="Fashion Sneakers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Fashion-Sneakers/zgbs/fashion/679312011/ref=zg_bs_nav_fashion_3_679255011')    
    child13_6_5_3 = tree.insert(child13_6_5, "end", text="Loafers & Slip-Ons", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Loafers-Slip-Ons/zgbs/fashion/679313011/ref=zg_bs_nav_fashion_3_679312011')    
    child13_6_5_4 = tree.insert(child13_6_5, "end", text="Mules & Clogs", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Mules-Clogs/zgbs/fashion/3420996011/ref=zg_bs_nav_fashion_3_679313011')    
    child13_6_5_5 = tree.insert(child13_6_5, "end", text="Outdoor")    
    tree.insert(child13_6_5_5, "end", text="Climbing", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Climbing-Shoes/zgbs/fashion/679270011/ref=zg_bs_nav_fashion_4_6127766011') 
    child13_6_5_5_0 = tree.insert(child13_6_5_5, "end", text="Hiking & Trekking") 
    tree.insert(child13_6_5_5_0, "end", text="Backpacking Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Backpacking-Boots/zgbs/fashion/3420956011/ref=zg_bs_nav_fashion_5_3420955011') 
    tree.insert(child13_6_5_5_0, "end", text="Hiking Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Hiking-Boots/zgbs/fashion/679280011/ref=zg_bs_nav_fashion_5_3420956011') 
    tree.insert(child13_6_5_5_0, "end", text="Hiking Shoes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Hiking-Shoes/zgbs/fashion/679282011/ref=zg_bs_nav_fashion_5_679280011') 
    tree.insert(child13_6_5_5_0, "end", text="Mountaineering Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Mountaineering-Boots/zgbs/fashion/679281011/ref=zg_bs_nav_fashion_5_679282011') 
    tree.insert(child13_6_5_5, "end", text="Hunting", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Hunting-Shoes/zgbs/fashion/679283011/ref=zg_bs_nav_fashion_4_6127766011') 
    child13_6_5_5_1 = tree.insert(child13_6_5_5, "end", text="Rain Footwear") 
    tree.insert(child13_6_5_5_1, "end", text="Rain", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Rain-Boots/zgbs/fashion/679266011/ref=zg_bs_nav_fashion_5_3420968011') 
    tree.insert(child13_6_5_5, "end", text="Snow Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Snow-Boots/zgbs/fashion/5658904011/ref=zg_bs_nav_fashion_4_6127766011') 
    tree.insert(child13_6_5_5, "end", text="Sport Sandals & Slides", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Athletic-Outdoor-Sandals-Slides/zgbs/fashion/679291011/ref=zg_bs_nav_fashion_4_5658904011') 
    tree.insert(child13_6_5_5, "end", text="Trail Running", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Trail-Running-Shoes/zgbs/fashion/1264575011/ref=zg_bs_nav_fashion_4_5658904011') 
    tree.insert(child13_6_5_5, "end", text="Water Shoes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Water-Shoes/zgbs/fashion/679304011/ref=zg_bs_nav_fashion_4_6127766011') 
    tree.insert(child13_6_5_5, "end", text="Western", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Western-Boots/zgbs/fashion/11721159011/ref=zg_bs_nav_fashion_4_6127766011') 
    tree.insert(child13_6_5, "end", text="Oxfords", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Oxfords/zgbs/fashion/679319011/ref=zg_bs_nav_fashion_3_679255011')    
    tree.insert(child13_6_5, "end", text="Sandals", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Sandals/zgbs/fashion/679320011/ref=zg_bs_nav_fashion_3_679319011')    
    child13_6_5_8 = tree.insert(child13_6_5, "end", text="Shoes")   
    tree.insert(child13_6_5_8, "end", text="Fire & Safety", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Fire-Safety-Shoes/zgbs/fashion/6796859011/ref=zg_bs_nav_fashion_5_679334011')  
    tree.insert(child13_6_5_8, "end", text="Health Care & Food Service", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Health-Care-Food-Service-Shoes/zgbs/fashion/6796861011/ref=zg_bs_nav_fashion_5_6796859011')  
    tree.insert(child13_6_5_8, "end", text="Military & Tactical", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Military-Tactical-Boots/zgbs/fashion/6796862011/ref=zg_bs_nav_fashion_5_6796861011')  
    tree.insert(child13_6_5_8, "end", text="Uniform Dress Shoes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Uniform-Dress-Shoes/zgbs/fashion/6796863011/ref=zg_bs_nav_fashion_5_6796862011')  
    child13_6_5_8_0 = tree.insert(child13_6_5_8, "end", text="Work & Utility")
    tree.insert(child13_6_5_8_0, "end", text="Industrial & Construction Bootsy", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Industrial-Construction-Boots/zgbs/fashion/11751044011/ref=zg_bs_nav_fashion_6_6796860011') 
    tree.insert(child13_6_5_8_0, "end", text="Shoes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Work-Utility-Shoes/zgbs/fashion/23721052011/ref=zg_bs_nav_fashion_6_11751044011')   
    tree.insert(child13_6_5, "end", text="Slippers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Slippers/zgbs/fashion/679324011/ref=zg_bs_nav_fashion_3_679320011')    
    child13_6_6 = tree.insert(child13_6, "end", text="Shops")
    child13_6_6_0 = tree.insert(child13_6_6, "end", text="Uniforms, Work & Safety")    
    child13_6_6_0_0 = tree.insert(child13_6_6_0, "end", text="Clothing")    
    child13_6_6_0_0_0 = tree.insert(child13_6_6_0_0, "end", text="Food Service") 
    tree.insert(child13_6_6_0_0_0, "end", text="Chef Jackets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Chef-Jackets/zgbs/fashion/6575931011/ref=zg_bs_nav_fashion_6_6575930011')    
    tree.insert(child13_6_6_0_0_0, "end", text="Chef Pants", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Chef-Pants/zgbs/fashion/6575932011/ref=zg_bs_nav_fashion_6_6575931011')    
    child13_6_6_0_0_1 = tree.insert(child13_6_6_0_0, "end", text="Medical") 
    tree.insert(child13_6_6_0_0_1, "end", text="Lab Coats", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Medical-Lab-Coats/zgbs/fashion/6567200011/ref=zg_bs_nav_fashion_6_6567198011')
    tree.insert(child13_6_6_0_0_1, "end", text="Scrub Bottoms", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Medical-Scrub-Pants/zgbs/fashion/6567201011/ref=zg_bs_nav_fashion_6_6567200011')
    tree.insert(child13_6_6_0_0_1, "end", text="Scrub Jackets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Medical-Scrub-Jackets/zgbs/fashion/6567202011/ref=zg_bs_nav_fashion_6_6567201011')
    tree.insert(child13_6_6_0_0_1, "end", text="Scrub Sets", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Medical-Scrub-Sets/zgbs/fashion/6567203011/ref=zg_bs_nav_fashion_6_6567202011')
    tree.insert(child13_6_6_0_0_1, "end", text="Scrub Tops", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Medical-Scrub-Shirts/zgbs/fashion/6567204011/ref=zg_bs_nav_fashion_6_6567203011')   
    child13_6_6_0_0_2 = tree.insert(child13_6_6_0_0, "end", text="Military")   
    tree.insert(child13_6_6_0_0_2, "end", text="Accessories", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Military-Accessories/zgbs/fashion/2492612011/ref=zg_bs_nav_fashion_6_2492606011') 
    tree.insert(child13_6_6_0_0_2, "end", text="Outerwear", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Military-Outerwear/zgbs/fashion/2492611011/ref=zg_bs_nav_fashion_6_2492612011') 
    tree.insert(child13_6_6_0_0_2, "end", text="Pants", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Military-Pants/zgbs/fashion/2492608011/ref=zg_bs_nav_fashion_6_2492611011') 
    tree.insert(child13_6_6_0_0_2, "end", text="Tops", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Military-Shirts/zgbs/fashion/2492607011/ref=zg_bs_nav_fashion_6_2492608011')  
    child13_6_6_0_0_3 = tree.insert(child13_6_6_0_0, "end", text="Work Utility & Safety")  
    tree.insert(child13_6_6_0_0_3, "end", text="Outerwear") 
    tree.insert(child13_6_6_0_0_3, "end", text="Overalls & Coveralls") 
    tree.insert(child13_6_6_0_0_3, "end", text="Pants") 
    tree.insert(child13_6_6_0_0_3, "end", text="Shorts") 
    tree.insert(child13_6_6_0_0_3, "end", text="Tops")   
    child13_6_6_0_1 = tree.insert(child13_6_6_0, "end", text="Shoes")    
    tree.insert(child13_6_6_0_1, "end", text="Fire & Safety", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Fire-Safety-Shoes/zgbs/fashion/6796859011/ref=zg_bs_nav_fashion_5_679334011')
    tree.insert(child13_6_6_0_1, "end", text="Health Care & Food Service", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Health-Care-Food-Service-Shoes/zgbs/fashion/6796861011/ref=zg_bs_nav_fashion_5_6796859011')
    tree.insert(child13_6_6_0_1, "end", text="Military & Tactical", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Military-Tactical-Boots/zgbs/fashion/6796862011/ref=zg_bs_nav_fashion_5_6796861011')
    tree.insert(child13_6_6_0_1, "end", text="Uniform Dress Shoes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Uniform-Dress-Shoes/zgbs/fashion/6796863011/ref=zg_bs_nav_fashion_5_6796862011')
    child13_6_6_0_1_0 = tree.insert(child13_6_6_0_1, "end", text="Work & Utility")
    tree.insert(child13_6_6_0_1_0, "end", text="Industrial & Construction Boots", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Industrial-Construction-Boots/zgbs/fashion/11751044011/ref=zg_bs_nav_fashion_6_6796860011')
    tree.insert(child13_6_6_0_1_0, "end", text="Shoes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Work-Utility-Shoes/zgbs/fashion/23721052011/ref=zg_bs_nav_fashion_6_11751044011')
    child13_6_7 = tree.insert(child13_6, "end", text="Watches")
    tree.insert(child13_6_7, "end", text="Pocket Watches", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Pocket-Watches/zgbs/fashion/6358542011/ref=zg_bs_nav_fashion_3_6358539011')    
    tree.insert(child13_6_7, "end", text="Smartwatches", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Smartwatches/zgbs/fashion/14130292011/ref=zg_bs_nav_fashion_3_6358542011')    
    tree.insert(child13_6_7, "end", text="Watch Bands", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Watch-Bands/zgbs/fashion/6358541011/ref=zg_bs_nav_fashion_3_14130292011')    
    tree.insert(child13_6_7, "end", text="Wrist Watches", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Wrist-Watches/zgbs/fashion/6358540011/ref=zg_bs_nav_fashion_3_6358541011')    
    
    child13_7 = tree.insert(parent_item13, "end", text="Novelty & More")
    child13_7_0 = tree.insert(child13_7, "end", text="All")
    child13_8 = tree.insert(parent_item13, "end", text="Shoe, Jewelry & Watch Accessories")
    child13_8_0 = tree.insert(child13_8, "end", text="Jewelry Accessories")
    tree.insert(child13_8_0, "end", text="Cleaning & Care", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Jewelry-Cleaning-Care-Products/zgbs/fashion/13830051/ref=zg_bs_nav_fashion_3_9616098011')
    child13_8_0_0 = tree.insert(child13_8_0, "end", text="Jewelry Boxes & Organizers")
    tree.insert(child13_8_0_0, "end", text="Children's Jewelry Boxes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Childrens-Jewelry-Boxes/zgbs/fashion/19431297011/ref=zg_bs_nav_fashion_4_3743851')
    tree.insert(child13_8_0_0, "end", text="Jewelry Armoires", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Jewelry-Armoires/zgbs/fashion/16350281/ref=zg_bs_nav_fashion_4_19431297011')
    tree.insert(child13_8_0_0, "end", text="Jewelry Boxes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Jewelry-Boxes/zgbs/fashion/16350291/ref=zg_bs_nav_fashion_4_16350281')
    tree.insert(child13_8_0_0, "end", text="Jewelry Chests", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Jewelry-Chests/zgbs/fashion/16350321/ref=zg_bs_nav_fashion_4_16350291')
    tree.insert(child13_8_0_0, "end", text="Jewelry Rolls", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Jewelry-Rolls/zgbs/fashion/3888531/ref=zg_bs_nav_fashion_4_16350321')
    tree.insert(child13_8_0_0, "end", text="Jewelry Towers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Jewelry-Towers/zgbs/fashion/16350341/ref=zg_bs_nav_fashion_4_3888531')
    tree.insert(child13_8_0_0, "end", text="Jewelry Trays", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Jewelry-Trays/zgbs/fashion/16350351/ref=zg_bs_nav_fashion_4_16350341')
    tree.insert(child13_8_0, "end", text="Loose Gemstones", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Loose-Gemstones/zgbs/fashion/8975615011/ref=zg_bs_nav_fashion_3_9616098011')
    tree.insert(child13_8_0, "end", text="Ring Sizers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Ring-Sizers/zgbs/fashion/21572176011/ref=zg_bs_nav_fashion_3_8975615011')
    child13_8_1 = tree.insert(child13_8, "end", text="Shoe Care & Accessories")
    tree.insert(child13_8_1, "end", text="Electric Shoe Polishers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Electric-Shoe-Polishers/zgbs/fashion/3743391/ref=zg_bs_nav_fashion_3_3421064011')
    tree.insert(child13_8_1, "end", text="Ice & Snow Grips", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Ice-Snow-Grips/zgbs/fashion/3421064011/ref=zg_bs_nav_fashion_3_3743391')
    child13_8_1_0 = tree.insert(child13_8_1, "end", text="Inserts & Insoles")
    tree.insert(child13_8_1_0, "end", text="Arch Supports", tags='https://www.amazon.com/Best-Sellers-Health-Household-Foot-Arch-Supports/zgbs/hpc/3780091/ref=zg_bs_nav_hpc_4_3780081')
    tree.insert(child13_8_1_0, "end", text="Ball-of-Foot Cushions", tags='https://www.amazon.com/Best-Sellers-Health-Household-Ball-of-Foot-Cushions/zgbs/hpc/3780101/ref=zg_bs_nav_hpc_4_3780091')
    tree.insert(child13_8_1_0, "end", text="Heel Cushions & Cups", tags='https://www.amazon.com/Best-Sellers-Health-Household-Heel-Cushions-Cups/zgbs/hpc/3780111/ref=zg_bs_nav_hpc_4_3780101')
    tree.insert(child13_8_1_0, "end", text="Insoles", tags='https://www.amazon.com/Best-Sellers-Health-Household-Shoe-Insoles/zgbs/hpc/3780121/ref=zg_bs_nav_hpc_4_3780111')
    tree.insert(child13_8_1, "end", text="Shoe & Boot Trees", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Boot-Trees/zgbs/fashion/3421050011/ref=zg_bs_nav_fashion_3_3421064011')
    tree.insert(child13_8_1, "end", text="Shoe Bags", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Bags/zgbs/fashion/15744061/ref=zg_bs_nav_fashion_3_3421050011')
    tree.insert(child13_8_1, "end", text="Shoe Brushes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Brushes/zgbs/fashion/3743401/ref=zg_bs_nav_fashion_3_3421050011')
    child13_8_1_1 = tree.insert(child13_8_1, "end", text="Shoe Care Treatments & Dyes")
    tree.insert(child13_8_1_1, "end", text="Dyes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Dyes/zgbs/fashion/3421048011/ref=zg_bs_nav_fashion_4_21614982011')
    tree.insert(child13_8_1_1, "end", text="Shoe Care Kits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Care-Kits/zgbs/fashion/3621779011/ref=zg_bs_nav_fashion_4_3421048011')
    child13_8_1_1_0 = tree.insert(child13_8_1_1, "end", text="Shoe Treatments & Polishes")
    tree.insert(child13_8_1_1_0, "end", text="Shoe Cleaners", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Cleaners/zgbs/fashion/21381610011/ref=zg_bs_nav_fashion_5_21381609011')
    tree.insert(child13_8_1_1_0, "end", text="Shoe Polishes", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Polishes/zgbs/fashion/21381609011/ref=zg_bs_nav_fashion_5_21381610011')
    tree.insert(child13_8_1_1_0, "end", text="Water & Stain Treatments", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Protective-Treatments/zgbs/fashion/21381608011/ref=zg_bs_nav_fashion_5_21381609011')
    tree.insert(child13_8_1, "end", text="Shoe Decoration Charms", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Decoration-Charms/zgbs/fashion/3421062011/ref=zg_bs_nav_fashion_3_3743401')
    tree.insert(child13_8_1, "end", text="Shoe Dryers", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Dryers/zgbs/fashion/3743411/ref=zg_bs_nav_fashion_3_3421062011')
    tree.insert(child13_8_1, "end", text="Shoe Horns & Boot Jacks", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Horns-Boot-Jacks/zgbs/fashion/3421055011/ref=zg_bs_nav_fashion_3_3743411')
    tree.insert(child13_8_1, "end", text="Shoe Measuring Devices", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoe-Measuring-Devices/zgbs/fashion/3421065011/ref=zg_bs_nav_fashion_3_3421055011')
    tree.insert(child13_8_1, "end", text="Shoelaces", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Shoelaces/zgbs/fashion/3421054011/ref=zg_bs_nav_fashion_3_3421065011')
    child13_8_2 = tree.insert(child13_8, "end", text="Watch Accessories")
    tree.insert(child13_8_2, "end", text="Cabinets & Cases", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Watch-Cabinets-Cases/zgbs/fashion/378530011/ref=zg_bs_nav_fashion_3_9616099011')
    tree.insert(child13_8_2, "end", text="Coin & Button Cell", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Coin-Button-Cell-Batteries/zgbs/fashion/389581011/ref=zg_bs_nav_fashion_3_378530011')
    tree.insert(child13_8_2, "end", text="Pocket Watch Chains", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Pocket-Watch-Chains/zgbs/fashion/378528011/ref=zg_bs_nav_fashion_3_378530011')
    tree.insert(child13_8_2, "end", text="Repair Tools & Kits", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Watch-Repair-Tools-Kits/zgbs/fashion/378531011/ref=zg_bs_nav_fashion_3_378528011')
    tree.insert(child13_8_2, "end", text="Watch Bands", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Mens-Watch-Bands/zgbs/fashion/6358541011/ref=zg_bs_nav_fashion_4_6909234011')
    tree.insert(child13_8_2, "end", text="Watch Winders", tags='https://www.amazon.com/Best-Sellers-Clothing-Shoes-Jewelry-Watch-Winders/zgbs/fashion/378532011/ref=zg_bs_nav_fashion_3_378531011')
    child13_9 = tree.insert(parent_item13, "end", text="Sport Specific Clothing")
    child13_9_0 = tree.insert(child13_9, "end", text="All")
    child13_10 = tree.insert(parent_item13, "end", text="Uniforms, Work & Safety")
    child13_10_0 = tree.insert(child13_10, "end", text="All")
    child13_11 = tree.insert(parent_item13, "end", text="Women")
    child13_11_0 = tree.insert(child13_11, "end", text="All")

    parent_item14 = tree.insert("", "end", text="Collectible Coins")
    child14_0 = tree.insert(parent_item14, "end", text="All")

    parent_item15 = tree.insert("", "end", text="Computers & Accessories")
    child15_0 = tree.insert(parent_item15, "end", text="All")

    parent_item16 = tree.insert("", "end", text="Digital Educational Resources")
    child16_0 = tree.insert(parent_item16, "end", text="All")

    parent_item17 = tree.insert("", "end", text="Digital Music")
    child17_0 = tree.insert(parent_item17, "end", text="All")

    parent_item18 = tree.insert("", "end", text="Electronics")
    child18_0 = tree.insert(parent_item18, "end", text="All")

    parent_item19 = tree.insert("", "end", text="Entertainment Collectibles")
    child19_0 = tree.insert(parent_item19, "end", text="All")

    parent_item20 = tree.insert("", "end", text="Gift Cards")
    child20_0 = tree.insert(parent_item20, "end", text="All")

    parent_item21 = tree.insert("", "end", text="Grocery & Gourmet Food")
    child21_0 = tree.insert(parent_item21, "end", text="All")

    parent_item22 = tree.insert("", "end", text="Handmade Products")
    child22 = tree.insert(parent_item22, "end", text="All", tags="https://www.amazon.com/Best-Sellers-Handmade-Products/zgbs/handmade/ref=zg_bs_nav_handmade_0")
    child22_0 = tree.insert(parent_item22, "end", text="Baby")
    child22_0_0 = tree.insert(child22_0, "end", text="All")
    child22_1 = tree.insert(parent_item22, "end", text="Beauty & Grooming")
    child22_1_0 = tree.insert(child22_1, "end", text="All")
    child22_2 = tree.insert(parent_item22, "end", text="Clothing, Shoes & Accessories")
    child22_2_0 = tree.insert(child22_2, "end", text="All")
    child22_3 = tree.insert(parent_item22, "end", text="Electronics Accessories")
    tree.insert(child22_3, "end", text="Camera & Photo Accessories", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Camera-Photo-Accessories/zgbs/handmade/14345424011/ref=zg_bs_nav_handmade_2_14345426011')
    tree.insert(child22_3, "end", text="Cell Phone Accessories", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Cell-Phone-Accessories/zgbs/handmade/14345426011/ref=zg_bs_nav_handmade_2_14345424011')
    child22_3_0 = tree.insert(child22_3, "end", text="Computer Accessories")
    tree.insert(child22_3_0, "end", text="Mouse Pads", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Computer-Mouse-Pads/zgbs/handmade/14345432011/ref=zg_bs_nav_handmade_3_14345430011')
    tree.insert(child22_3_0, "end", text="Wrist Rests", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Computer-Wrist-Rests/zgbs/handmade/14345433011/ref=zg_bs_nav_handmade_3_14345432011')
    tree.insert(child22_3, "end", text="Fitness Tracker Bands & Straps", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Fitness-Tracker-Bands-Straps/zgbs/handmade/18730253011/ref=zg_bs_nav_handmade_2_11403474011')
    child22_3_1 = tree.insert(child22_3, "end", text="Laptop Accessories")
    child22_3_1_0 = tree.insert(child22_3_1, "end", text="Bags, Cases & Sleeves")
    tree.insert(child22_3_1_0, "end", text="Briefcases", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Laptop-Netbook-Briefcases/zgbs/handmade/14345442011/ref=zg_bs_nav_handmade_4_14345440011')
    tree.insert(child22_3_1_0, "end", text="Hard Case Shells", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Laptop-Netbook-Hard-Case-Shells/zgbs/handmade/14345443011/ref=zg_bs_nav_handmade_4_14345442011')
    tree.insert(child22_3_1_0, "end", text="Messenger & Shoulder Bags", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Laptop-Netbook-Messenger-Shoulder-Bags/zgbs/handmade/14345444011/ref=zg_bs_nav_handmade_4_14345443011')
    tree.insert(child22_3_1_0, "end", text="Sleeves", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Laptop-Netbook-Sleeves/zgbs/handmade/14345447011/ref=zg_bs_nav_handmade_4_14345444011')
    tree.insert(child22_3_1, "end", text="Skins & Decals", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Laptop-Netbook-Skins-Decals/zgbs/handmade/14345449011/ref=zg_bs_nav_handmade_3_14345439011')
    child22_4 = tree.insert(parent_item22, "end", text="Health & Personal Care")
    child22_4_0 = tree.insert(child22_4, "end", text="Personal Care")
    child22_4_0_0 = tree.insert(child22_4_0, "end", text="Bath & Bathing Accessories")
    child22_4_1 = tree.insert(child22_4, "end", text="Wellness & Relaxation")
    child22_5 = tree.insert(parent_item22, "end", text="Home & Kitchen")
    child22_5_0 = tree.insert(child22_5, "end", text="All")
    child22_6 = tree.insert(parent_item22, "end", text="Jewelry")
    child22_6_0 = tree.insert(child22_6, "end", text="All")
    child22_7 = tree.insert(parent_item22, "end", text="Pet Supplies")
    child22_7_0 = tree.insert(child22_7, "end", text="All")
    child22_8 = tree.insert(parent_item22, "end", text="Sports & Outdoors")
    child22_8_0 = tree.insert(child22_8, "end", text="All")
    child22_9 = tree.insert(parent_item22, "end", text="Stationery & Party Supplies")
    child22_9_0 = tree.insert(child22_9, "end", text="Party Supplies")
    tree.insert(child22_9_0, "end", text="Aisle Runners", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Aisle-Runners/zgbs/handmade/16495852011/ref=zg_bs_nav_handmade_3_11435471011')
    tree.insert(child22_9_0, "end", text="Centerpieces", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Centerpieces/zgbs/handmade/11435472011/ref=zg_bs_nav_handmade_3_16495852011')
    tree.insert(child22_9_0, "end", text="Ceremony Programs", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Ceremony-Programs/zgbs/handmade/16578958011/ref=zg_bs_nav_handmade_3_11435472011')
    tree.insert(child22_9_0, "end", text="Confetti", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Confetti/zgbs/handmade/16495853011/ref=zg_bs_nav_handmade_3_16578958011')
    tree.insert(child22_9_0, "end", text="Decorations", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Decorations/zgbs/handmade/11435473011/ref=zg_bs_nav_handmade_3_16495853011')
    tree.insert(child22_9_0, "end", text="Garlands & Decorative Banners", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Garlands-Decorative-Banners/zgbs/handmade/16495854011/ref=zg_bs_nav_handmade_3_11435473011')
    tree.insert(child22_9_0, "end", text="Menu Cards", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Menu-Cards/zgbs/handmade/16578956011/ref=zg_bs_nav_handmade_3_16495854011')
    tree.insert(child22_9_0, "end", text="Party Favors", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Party-Favors/zgbs/handmade/11435476011/ref=zg_bs_nav_handmade_3_16578956011')
    tree.insert(child22_9_0, "end", text="Place Cards", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Place-Cards/zgbs/handmade/11435480011/ref=zg_bs_nav_handmade_3_11435476011')
    tree.insert(child22_9_0, "end", text="Table Numbers", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Table-Numbers/zgbs/handmade/16495855011/ref=zg_bs_nav_handmade_3_11435480011')
    tree.insert(child22_9, "end", text="Pens & Pencils", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Pens-Pencils/zgbs/handmade/11435481011/ref=zg_bs_nav_handmade_2_11435470011')    
    child22_9_2 = tree.insert(child22_9, "end", text="Stationery")
    tree.insert(child22_9_2, "end", text="Appointment Books & Planners", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Appointment-Books-Planners/zgbs/handmade/13542491011/ref=zg_bs_nav_handmade_3_11435484011')
    tree.insert(child22_9_2, "end", text="Books & Journals", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Books-Journals/zgbs/handmade/11438774011/ref=zg_bs_nav_handmade_3_13542491011')
    tree.insert(child22_9_2, "end", text="Gift Tags", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Gift-Tags/zgbs/handmade/13542500011/ref=zg_bs_nav_handmade_3_11438774011')
    tree.insert(child22_9_2, "end", text="Gift Wrapping Paper", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Gift-Wrapping-Paper/zgbs/handmade/11435487011/ref=zg_bs_nav_handmade_3_13542500011')
    tree.insert(child22_9_2, "end", text="Invitations", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Invitations/zgbs/handmade/11435485011/ref=zg_bs_nav_handmade_3_11435487011')
    tree.insert(child22_9_2, "end", text="Labels", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Labels/zgbs/handmade/13542501011/ref=zg_bs_nav_handmade_3_11435485011')
    tree.insert(child22_9_2, "end", text="Notecards & Greeting Cards", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Notecards-Greeting-Cards/zgbs/handmade/11435486011/ref=zg_bs_nav_handmade_3_13542501011')
    tree.insert(child22_9_2, "end", text="Paper", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Paper/zgbs/handmade/11435488011/ref=zg_bs_nav_handmade_3_11435486011')
    tree.insert(child22_9_2, "end", text="Stamps", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Stamps/zgbs/handmade/11435490011/ref=zg_bs_nav_handmade_3_11435488011')
    tree.insert(child22_9_2, "end", text="Stickers", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Stickers/zgbs/handmade/11435491011/ref=zg_bs_nav_handmade_3_11435490011')
    tree.insert(child22_9_2, "end", text="Wall Calendars", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Wall-Calendars/zgbs/handmade/13542490011/ref=zg_bs_nav_handmade_3_11435491011')
    child22_10 = tree.insert(parent_item22, "end", text="Toys & Games")
    tree.insert(child22_10, "end", text="Baby & Toddler Toys", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Baby-Toddler-Toys/zgbs/handmade/14351279011/ref=zg_bs_nav_handmade_2_11403495011')
    tree.insert(child22_10, "end", text="Dolls, Toy Figures & Accessories", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Dolls-Toy-Figures-Accessories/zgbs/handmade/14351291011/ref=zg_bs_nav_handmade_2_14351279011')
    tree.insert(child22_10, "end", text="Lawn & Playground", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Lawn-Games-Playground-Equipment/zgbs/handmade/14351342011/ref=zg_bs_nav_handmade_2_14351291011')
    tree.insert(child22_10, "end", text="Learning & Education", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Childrens-Learning-Development-Toys/zgbs/handmade/14351318011/ref=zg_bs_nav_handmade_2_14351342011')
    tree.insert(child22_10, "end", text="Musical Toy Instruments", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Toy-Musical-Instruments/zgbs/handmade/14351319011/ref=zg_bs_nav_handmade_2_14351318011')
    child22_10_0 = tree.insert(child22_10, "end", text="Novelty & Gag Toys")
    tree.insert(child22_10_0, "end", text="Magnets & Magnetic Toys", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Magnet-Magnetic-Toys/zgbs/handmade/14351325011/ref=zg_bs_nav_handmade_3_14351320011')
    tree.insert(child22_10_0, "end", text="Money Banks", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Money-Banks/zgbs/handmade/14351327011/ref=zg_bs_nav_handmade_3_14351325011')
    tree.insert(child22_10_0, "end", text="Temporary Tattoos", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Childrens-Temporary-Tattoos/zgbs/handmade/14351331011/ref=zg_bs_nav_handmade_3_14351327011')
    tree.insert(child22_10, "end", text="Plushies & Stuffed Animals", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Stuffed-Animals-Plushies/zgbs/handmade/14351334011/ref=zg_bs_nav_handmade_2_11403495011')
    tree.insert(child22_10, "end", text="Pretend Play", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Pretend-Play-Toys/zgbs/handmade/14351335011/ref=zg_bs_nav_handmade_2_14351334011')
    tree.insert(child22_10, "end", text="Puppets", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Puppets/zgbs/handmade/14351336011/ref=zg_bs_nav_handmade_2_14351335011')
    tree.insert(child22_10, "end", text="Puzzles", tags='https://www.amazon.com/Best-Sellers-Handmade-Products-Handmade-Puzzles/zgbs/handmade/14351341011/ref=zg_bs_nav_handmade_2_14351336011')

    parent_item23 = tree.insert("", "end", text="Health & Household")
    child23_0 = tree.insert(parent_item23, "end", text="All")

    parent_item24 = tree.insert("", "end", text="Home & Kitchen")
    child24_0 = tree.insert(parent_item24, "end", text="All")


    parent_item25 = tree.insert("", "end", text="Industrial & Scientific")
    child25_0 = tree.insert(parent_item25, "end", text="All")

    parent_item26 = tree.insert("", "end", text="Kindle Store")
    child26_0 = tree.insert(parent_item26, "end", text="All")

    parent_item27 = tree.insert("", "end", text="Kitchen & Dining")
    child27_0 = tree.insert(parent_item27, "end", text="All")

    parent_item28 = tree.insert("", "end", text="Movies & TV")
    child28_0 = tree.insert(parent_item28, "end", text="All")


    parent_item29 = tree.insert("", "end", text="Musical Instruments")
    child29_0 = tree.insert(parent_item29, "end", text="All")


    parent_item30 = tree.insert("", "end", text="Office Products")
    child30_0 = tree.insert(parent_item30, "end", text="All")


    parent_item31 = tree.insert("", "end", text="Patio, Lawn & Garden")
    child31_0 = tree.insert(parent_item31, "end", text="All")


    parent_item32 = tree.insert("", "end", text="Pet Supplies")
    child32_0 = tree.insert(parent_item32, "end", text="All")


    parent_item33 = tree.insert("", "end", text="Software")
    child33_0 = tree.insert(parent_item33, "end", text="All")


    parent_item34 = tree.insert("", "end", text="Sports & Outdoors")
    child34_0 = tree.insert(parent_item34, "end", text="All")


    parent_item35 = tree.insert("", "end", text="Sports Collectibles")
    child35_0 = tree.insert(parent_item35, "end", text="All")


    parent_item36 = tree.insert("", "end", text="Tools & Home Improvement")
    child36_0 = tree.insert(parent_item36, "end", text="All")


    parent_item37 = tree.insert("", "end", text="Toys & Games")
    child37_0 = tree.insert(parent_item37, "end", text="All")

    parent_item38 = tree.insert("", "end", text="Unique Finds")
    child38_0 = tree.insert(parent_item38, "end", text="All")


    parent_item39 = tree.insert("", "end", text="Video Games")
    child39_0 = tree.insert(parent_item39, "end", text="All")

    
    

    # Update the canvas window to fit the contents
    tree.update_idletasks()
    canvas.create_window((0, 0), window=tree_frame, anchor="nw")

    # Configure the Canvas to scroll
    canvas.config(scrollregion=canvas.bbox("all"))  


    canvas.create_text(
        400.0,
        150.0,
        anchor="nw",
        text="IP address",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )
    canvas.create_text(
        560.0,
        150.0,
        anchor="nw",
        text="PORT",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )
    canvas.create_text(
        690.0,
        150.0,
        anchor="nw",
        text="USERNAME",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )
    canvas.create_text(
        860.0,
        150.0,
        anchor="nw",
        text="PASSWORD",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    IP_address1_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    IP_address1_entry.place(
        x=350.0,
        y=200,
        width=170.0,
        height=30.0
    )

    PORT1_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PORT1_entry.place(
        x=530.0,
        y=200,
        width=100.0,
        height=30.0
    )

    USERNAME1_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    USERNAME1_entry.place(
        x=645.0,
        y=200,
        width=170.0,
        height=30.0
    )

    PASSWORD1_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PASSWORD1_entry.place(
        x=820.0,
        y=200,
        width=170.0,
        height=30.0
    )

    canvas.create_text(
        270.0,
        207.0,
        anchor="nw",
        text="Proxy 1",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    IP_address2_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    IP_address2_entry.place(
        x=350.0,
        y=255,
        width=170.0,
        height=30.0
    )

    PORT2_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PORT2_entry.place(
        x=530.0,
        y=255,
        width=100.0,
        height=30.0
    )

    USERNAME2_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    USERNAME2_entry.place(
        x=645.0,
        y=255,
        width=170.0,
        height=30.0
    )

    PASSWORD2_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PASSWORD2_entry.place(
        x=820.0,
        y=255,
        width=170.0,
        height=30.0
    )

    canvas.create_text(
        270.0,
        262.0,
        anchor="nw",
        text="Proxy 2",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    IP_address3_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    IP_address3_entry.place(
        x=350.0,
        y=310,
        width=170.0,
        height=30.0
    )

    PORT3_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PORT3_entry.place(
        x=530.0,
        y=310,
        width=100.0,
        height=30.0
    )

    USERNAME3_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    USERNAME3_entry.place(
        x=645.0,
        y=310,
        width=170.0,
        height=30.0
    )

    PASSWORD3_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )
    PASSWORD3_entry.place(
        x=820.0,
        y=310,
        width=170.0,
        height=30.0
    )

    canvas.create_text(
        270.0,
        317.0,
        anchor="nw",
        text="Proxy 3",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    canvas.create_text(
        575.0,
        480.0,
        anchor="nw",
        text="Console Log",
        fill="#000000",
        font=("Roboto Medium", 14 * -1)
    )

    console_entry = Entry(
        bd=0,
        bg="#ebe6e6",
        fg="#000000",
        highlightthickness=0
    )

    console_entry.place(
        x=219.0,
        y=525,
        width=781.0,
        height=100.0
    )


    start_img = PhotoImage(file=relative_to_assets("start.png"))
    start_btn = Button(
        image=start_img, borderwidth=0, highlightthickness=0, relief="flat",command=lambda : start_function(), activebackground= "#202020")
    start_btn.place(x=75, y=720, width=100, height=47)

    stop_img = PhotoImage(file=relative_to_assets("stop.png"))    
    stop_btn = Button(image=stop_img, borderwidth=0, highlightthickness=0, relief="flat", command=lambda : stop_function(), activebackground= "#202020")
    stop_btn.place(x=825, y=720, width=100, height=47)   
    
    window.resizable(False, False)
    # Run the main event loop to display the window
    window.mainloop()
BuildingGUI()


        