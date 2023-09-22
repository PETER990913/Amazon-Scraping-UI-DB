from tkinter import Canvas, Entry, Text,  Button, PhotoImage,filedialog,END,Variable,messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path


# Initializing the global variants

item_text = ""
item_link = ""

# defining the Scrape function

def scrape_site():    
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
    import pandas as pd
    import time
    import re
    import logging
    
    logging.getLogger('webdriver_manager').disabled = True
    
    SCRAPEOPS_API_KEY = 'ab147e77-85aa-4e7f-8be4-6f1b2a685d62'

    proxy_options = {
        'proxy': {
            'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
            'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
            'no_proxy': 'localhost:127.0.0.1'
        }
    }
    # initial result values
    Product_title_list = []
    Product_image_URL_list = []
    Product_brand_list = []
    Product_Rate_list = []
    Product_Rating_list = []
    Product_price_list = []
    Product_package_list = []
    Product_department_list = []
    Product_date_list = []
    Product_ASIN_list = []
    Product_BSR_list = []
    Product_Month_list = []
    # Defining XPATH, CLASSNAME etc...
    Product_tables_class_name = 'zg-grid-general-faceout'
    Product_image_URL_XPATH = '//*[@id="landingImage"]'
    Product_brand_XPATH = '//*[@id="bylineInfo"]'
    Product_Rate_XPATH = '//*[@id="acrPopover"]/span[1]/a/span'
    Product_Rating_XPATH = '//*[@id="acrCustomerReviewText"]'    
    Product_price_Class1 = '_cDEzb_p13n-sc-price_3mJ9Z'
    Product_price_Class2 = 'p13n-sc-price'
    Next_page_XPATH = '//*[@id="CardInstanceVCC9iK3UsqjMrhI_ELT2fA"]/div[2]/div[2]/ul/li[4]'
    Product_BSR_XPATH = '//*[@id="detailBulletsWrapper_feature_div"]/ul[1]/li/span/ul/li/span'
    Product_Month_Sold_XPATH = '//*[@id="social-proofing-faceout-title-tk_bought"]/span'
    
    print("link", item_link[0])
    
    print('--------------------Automation scraping is successfully started-------------------')
    driver = webdriver.Chrome(seleniumwire_options=proxy_options)
    # driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    URL = item_link[0]
    driver.get(URL)  
    j = 0    
    while j<2:
        tables = driver.find_elements(By.CLASS_NAME, Product_tables_class_name)
        print(len(tables))
        for table in tables:
            try:
                Product_URL = table.find_elements(By.TAG_NAME, 'a')[0].get_attribute('href')
            except:
                Product_URL = "none"
            print("Product_image_URL", Product_URL)
            # Getting the product title
            try:
                Product_title = table.find_elements(By.TAG_NAME, 'a')[1].find_elements(By.TAG_NAME, 'span')[0].text
            except:
                Product_title = "none"
            print("Product_title:", Product_title)
            
            # Getting the product price
            try:
                try:
                    Product_price = table.find_element(By.CLASS_NAME, Product_price_Class1).text
                except:
                    Product_price = table.find_element(By.CLASS_NAME, Product_price_Class2).text                  
            except:
                Product_price = "none"
            print("Product_price:", Product_price)
            driver1 = webdriver.Chrome(seleniumwire_options=proxy_options)
            # driver1 = uc.Chrome(driver_executable_path=ChromeDriverManager().install())
            driver1.maximize_window()
            driver1.get(Product_URL)  
            
            try:
                Product_image_URL = driver1.find_element(By.XPATH, Product_image_URL_XPATH).get_attribute('src')
            except:
                Product_image_URL = "none"
            print("Product_image_URL:", Product_image_URL)
            try:
                Product_brand = driver1.find_element(By.XPATH, Product_brand_XPATH).text
                if ("Brand" in Product_brand):
                    Product_brand = str(Product_brand).replace('Brand:', '').replace(' ', '')
                else:
                    Product_brand = "none"
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
            
            product_detail = driver1.find_element(By.XPATH, '//*[@id="detailBullets_feature_div"]/ul')
            firsttables = product_detail.find_elements(By.CLASS_NAME, 'a-list-item')
            for firsttable in firsttables:
                item = firsttable.find_element(By.CLASS_NAME, 'a-text-bold').text
                print("item", item)
                if ('Package' in item):
                    Product_package = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                    print('Product_package:', Product_package)
                if ('Department' in item):
                    Product_department = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                    print('Product_department', Product_department)
                if ('Date:' in item):
                    Product_date = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                    print('Product_date:', Product_date)
                if ('ASIN' in item):
                    Product_ASIN = firsttable.find_elements(By.TAG_NAME, 'span')[1].text
                    print('Product_ASIN:', Product_ASIN)
                else:
                    Product_package = "none"            
                    Product_department = "none"            
                    Product_date = "none"            
                    Product_ASIN = "none"            
            try:
                Product_BSR = driver1.find_element(By.XPATH, Product_BSR_XPATH).text
                Product_BSR = str(Product_BSR).split('\n')[0].replace(' ', '').replace('in', '')
            except:
                Product_BSR = "none"
            print("Product_BSR", Product_BSR)
            Product_title_list.append(Product_title)             
            Product_image_URL_list.append(Product_image_URL)
            Product_brand_list.append(Product_brand)
            Product_Rate_list.append(Product_Rate)
            Product_Rating_list.append(Product_Rating)
            Product_price_list.append(Product_price)
            Product_package_list.append(Product_package)
            Product_department_list.append(Product_department)
            Product_date_list.append(Product_date)
            Product_ASIN_list.append(Product_ASIN)
            Product_BSR_list.append(Product_BSR)
            Product_Month_list.append(Product_Month)
            
            driver1.close()   
        j += 1
        try:
            driver.find_element(By.XPATH, Next_page_XPATH).click()
        except:
            print("can't find the next button anymore")  
    print('--------------------Automation scraping is successfully finished--------------------')   
    # Saving as EXCEL file
    dict = {'Product_title': Product_title_list, 'Product_image_URL': Product_image_URL_list, 'Product_brand': Product_brand_list,
            'Product_Rate': Product_Rate_list, 'Product_Rating': Product_Rating_list, 'Product_price': Product_price_list, 'Product_package_dimensions':Product_package_list, 'Product_department': Product_department_list, 'Product_Date_Available': Product_date_list,
            'Product_ASIN': Product_ASIN_list, 'Product_BSR': Product_BSR_list, 'Number of sold of in a month': Product_Month_list}
    df = pd.DataFrame(dict)
    df.to_csv('Result.csv') 
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
    def on_select(event):
        global item_link, item_text
        selected_item = tree.selection()[0]
        item_text = tree.item(selected_item)['text']
        item_link = tree.item(selected_item)['tags']
        # scrape_site(item_link)
        # return item_text, item_link   
    
    # Insert data into the Treeview
    parent_item = tree.insert("", "end", text="Amazon Devices & Accessories")
    child_0 = tree.insert(parent_item, "end", text="All", tags="https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories/zgbs/amazon-devices/ref=zg_bs_nav_amazon-devices_0")
    child_1 = tree.insert(parent_item, "end", text="Amazon Device Accessories")
    tree.insert(child_1, "end", text="All", tags="https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Accessories/zgbs/amazon-devices/370783011/ref=zg_bs_nav_amazon-devices_1")
    tree.insert(child_1, "end", text="Adapters & Connectors", tag="https://www.amazon.com/Best-Sellers-Amazon-Devices-Accessories-Amazon-Device-Adapters-Connectors/zgbs/amazon-devices/17942903011/ref=zg_bs_nav_amazon-devices_2_1289283011")
    tree.insert(child_1, "end", text="Audio")
    tree.insert(child_1, "end", text="Bases & Stands")
    tree.insert(child_1, "end", text="Charging Docks")
    tree.insert(child_1, "end", text="Clocks")
    tree.insert(child_1, "end", text="Covers")
    tree.insert(child_1, "end", text="Gaming Controllers")
    tree.insert(child_1, "end", text="Home Security Decals & Signs")
    tree.insert(child_1, "end", text="Home Security Solar Chargers")
    tree.insert(child_1, "end", text="Keyboards")
    tree.insert(child_1, "end", text="Memory Cards")
    tree.insert(child_1, "end", text="Mounts")
    tree.insert(child_1, "end", text="Power Supplies & Chargers")
    tree.insert(child_1, "end", text="Projection Mats")
    tree.insert(child_1, "end", text="Protection Plans")
    tree.insert(child_1, "end", text="Reading Lights")
    tree.insert(child_1, "end", text="Remote Controls")
    tree.insert(child_1, "end", text="Screen Protectors")
    tree.insert(child_1, "end", text="Skins")
    tree.insert(child_1, "end", text="Sleeves")
    tree.insert(child_1, "end", text="Styluses")
    tree.insert(child_1, "end", text="Tangrams")
    child_2 = tree.insert(parent_item, "end", text="Amazon Devices")
    tree.insert(child_2, "end", text="All")
    tree.insert(child_2, "end", text="Astro Household Robots")
    tree.insert(child_2, "end", text="Car Dash Cameras")
    tree.insert(child_2, "end", text="Device Bundles")
    tree.insert(child_2, "end", text="Echo Smart Speakers & Displays")
    tree.insert(child_2, "end", text="Fire TV")
    tree.insert(child_2, "end", text="Fire Tablets")
    tree.insert(child_2, "end", text="Home Wi-Fi & Networking")
    tree.insert(child_2, "end", text="Kindle E-readers")
    tree.insert(child_2, "end", text="Programmable Devices")
    tree.insert(child_2, "end", text="Sleep Trackers")
    tree.insert(child_2, "end", text="Smart Appliances")
    tree.insert(child_2, "end", text="Smart Home Security & Lighting")
    tree.insert(child_2, "end", text="Wearable Technology")

    parent_item1 = tree.insert("", "end", text="Amazon Renewed")

    parent_item2 = tree.insert("", "end", text="Appliances")
    tree.insert(parent_item2, "end", text="All")
    tree.insert(parent_item2, "end", text="Astro Household Robots")
    tree.insert(parent_item2, "end", text="Cooktops")
    tree.insert(parent_item2, "end", text="Dishwashers")
    tree.insert(parent_item2, "end", text="Freezers")
    tree.insert(parent_item2, "end", text="Ice Makers")
    tree.insert(parent_item2, "end", text="Range Hoods")
    tree.insert(parent_item2, "end", text="Ranges")
    tree.insert(parent_item2, "end", text="Refrigerators")
    tree.insert(parent_item2, "end", text="Wall Ovens")
    tree.insert(parent_item2, "end", text="Warming Drawers")
    tree.insert(parent_item2, "end", text="Washers & Dryers")
    tree.insert(parent_item2, "end", text="Wine Cellars")

    parent_item3 = tree.insert("", "end", text="Apps & Games")
    child3_0 = tree.insert(parent_item3, "end", text="All")
    child3_1 = tree.insert(parent_item3, "end", text="Books & Comics")
    tree.insert(child3_1, "end", text="All")
    tree.insert(child3_1, "end", text="Book Info & Reviews")
    tree.insert(child3_1, "end", text="Readers & Players")
    child3_2 = tree.insert(parent_item3, "end", text="Business")
    tree.insert(child3_2, "end", text="All")
    tree.insert(child3_2, "end", text="Accounting & Expenses")
    tree.insert(child3_2, "end", text="Banking")
    tree.insert(child3_2, "end", text="Currency Converters & Guides")
    tree.insert(child3_2, "end", text="Payments & Money Transfers")
    tree.insert(child3_2, "end", text="Personal Finance")
    tree.insert(child3_2, "end", text="Stocks & Investing")
    tree.insert(child3_2, "end", text="Tax Calculators")
    child3_3 = tree.insert(parent_item3, "end", text="Communication")
    child3_4 = tree.insert(parent_item3, "end", text="Customization")
    tree.insert(child3_4, "end", text="All")
    tree.insert(child3_4, "end", text="Ringtones & Notifications")
    tree.insert(child3_4, "end", text="Themes")
    tree.insert(child3_4, "end", text="Wallpapers & Images")
    tree.insert(child3_4, "end", text="Widgets")
    child3_5 = tree.insert(parent_item3, "end", text="Education")
    child3_6 = tree.insert(parent_item3, "end", text="Finance")
    tree.insert(child3_6, "end", text="All")
    tree.insert(child3_6, "end", text="Accounting & Expenses")
    tree.insert(child3_6, "end", text="Banking")
    tree.insert(child3_6, "end", text="Currency Converters & Guides")
    tree.insert(child3_6, "end", text="Payments & Money Transfers")
    tree.insert(child3_6, "end", text="Personal Finance")
    tree.insert(child3_6, "end", text="Stocks & Investing")
    tree.insert(child3_6, "end", text="Tax Calculators")
    child3_7 = tree.insert(parent_item3, "end", text="Food & Drink")
    tree.insert(child3_7, "end", text="All")
    tree.insert(child3_7, "end", text="Cooking & Recipes")
    tree.insert(child3_7, "end", text="Wine & Beverages")
    child3_8 = tree.insert(parent_item3, "end", text="Games")
    tree.insert(child3_8, "end", text="All")
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
    tree.insert(child3_9, "end", text="All")
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
    tree.insert(child3_10, "end", text="All")
    tree.insert(child3_10, "end", text="Book Readers & Players")
    tree.insert(child3_10, "end", text="Education")
    tree.insert(child3_10, "end", text="Games")
    tree.insert(child3_10, "end", text="Movie & TV Streaming")
    tree.insert(child3_10, "end", text="Music & Audio")
    child3_11 = tree.insert(parent_item3, "end", text="Lifestyle")
    tree.insert(child3_11, "end", text="All")
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
    tree.insert(child3_12, "end", text="All")
    tree.insert(child3_12, "end", text="Business Locators")
    tree.insert(child3_12, "end", text="Navigation")
    tree.insert(child3_12, "end", text="Offline Maps")
    tree.insert(child3_12, "end", text="Real Estate")
    tree.insert(child3_12, "end", text="Taxi & Ridesharing")
    child3_13 = tree.insert(parent_item3, "end", text="Magazines")
    child3_14 = tree.insert(parent_item3, "end", text="Medical")
    tree.insert(child3_14, "end", text="All")
    tree.insert(child3_14, "end", text="Education")
    tree.insert(child3_14, "end", text="Heart Rate Monitors")
    tree.insert(child3_14, "end", text="Massage Guides")
    tree.insert(child3_14, "end", text="Menstrual Trackers")
    tree.insert(child3_14, "end", text="Pregnancy")
    tree.insert(child3_14, "end", text="Reference")
    tree.insert(child3_14, "end", text="Sleep Tracking")
    child3_15 = tree.insert(parent_item3, "end", text="Movies & TV")
    tree.insert(child3_15, "end", text="All")
    tree.insert(child3_15, "end", text="Movie Info & Reviews")
    tree.insert(child3_15, "end", text="On-Demand Movie Streaming")
    tree.insert(child3_15, "end", text="Video-Sharing")
    child3_16 = tree.insert(parent_item3, "end", text="Music & Audio")
    tree.insert(child3_16, "end", text="All")
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
    tree.insert(child3_17, "end", text="All")
    tree.insert(child3_17, "end", text="Feed Aggregators")
    tree.insert(child3_17, "end", text="Newspapers")
    tree.insert(child3_17, "end", text="Sports Fan News")
    child3_18 = tree.insert(parent_item3, "end", text="Novelty")
    tree.insert(child3_18, "end", text="All")
    tree.insert(child3_18, "end", text="Funny Pictures")
    tree.insert(child3_18, "end", text="Funny Sounds")
    tree.insert(child3_18, "end", text="Prank Biometric Scanners")
    tree.insert(child3_18, "end", text="Screen Pranks")
    tree.insert(child3_18, "end", text="Talking & Answering")
    child3_19 = tree.insert(parent_item3, "end", text="Photo & Video")
    child3_20 = tree.insert(parent_item3, "end", text="Productivity")
    tree.insert(child3_20, "end", text="All")
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
    tree.insert(child3_21, "end", text="All")
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
    tree.insert(child3_23, "end", text="All")
    tree.insert(child3_23, "end", text="Blogging")
    tree.insert(child3_23, "end", text="Dating")
    tree.insert(child3_23, "end", text="Email Clients")
    tree.insert(child3_23, "end", text="General Social Networking")
    tree.insert(child3_23, "end", text="Photo-Sharing")
    tree.insert(child3_23, "end", text="Professional Networking")
    tree.insert(child3_23, "end", text="Social Network Management")
    tree.insert(child3_23, "end", text="Video-Sharing")
    child3_24 = tree.insert(parent_item3, "end", text="Sports")
    tree.insert(child3_24, "end", text="All")
    tree.insert(child3_24, "end", text="Activity Tracking")
    tree.insert(child3_24, "end", text="Exercise Motivation")
    tree.insert(child3_24, "end", text="Heart Rate Monitors")
    tree.insert(child3_24, "end", text="Sports Fan News")
    tree.insert(child3_24, "end", text="Sports Games")
    tree.insert(child3_24, "end", text="Sports Information")
    tree.insert(child3_24, "end", text="Workout Guides")
    tree.insert(child3_24, "end", text="Yoga Guides")
    child3_25 = tree.insert(parent_item3, "end", text="Transportation")
    tree.insert(child3_25, "end", text="All")
    tree.insert(child3_25, "end", text="Auto Rental")
    tree.insert(child3_25, "end", text="Flight Finders")
    tree.insert(child3_25, "end", text="Navigation")
    tree.insert(child3_25, "end", text="Taxi & Ridesharing")
    child3_26 = tree.insert(parent_item3, "end", text="Travel")
    tree.insert(child3_26, "end", text="All")
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
    tree.insert(child3_27, "end", text="All")
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
    child11_0 = tree.insert(parent_item11, "end", text="All")

    parent_item12 = tree.insert("", "end", text="Climate Pledge Friendly")
    child12_0 = tree.insert(parent_item12, "end", text="All")

    parent_item13 = tree.insert("", "end", text="Clothing, Shoes & Jewelry")
    child13_0 = tree.insert(parent_item13, "end", text="All")
    child13_1 = tree.insert(parent_item13, "end", text="Baby")
    child13_2 = tree.insert(parent_item13, "end", text="Boys")
    child13_3 = tree.insert(parent_item13, "end", text="Costumes & Accessories")
    child13_4 = tree.insert(parent_item13, "end", text="Girls")
    child13_5 = tree.insert(parent_item13, "end", text="Luggage & Travel Gear")
    child13_6 = tree.insert(parent_item13, "end", text="Men")
    child13_6_0 = tree.insert(child13_6, "end", text="All")
    child13_6_1 = tree.insert(child13_6, "end", text="Accessories")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="Belts")
    tree.insert(child13_6_1, "end", text="Collar Stays")
    tree.insert(child13_6_1, "end", text="Cuff Links, Shirt Studs & Tie Clips")
    tree.insert(child13_6_1, "end", text="Earmuffs")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    tree.insert(child13_6_1, "end", text="All")
    child13_6_2 = tree.insert(child13_6, "end", text="Clothing")
    child13_6_3 = tree.insert(child13_6, "end", text="Handbags & Shoulder Bags")
    child13_6_4 = tree.insert(child13_6, "end", text="Jewelry")
    child13_6_5 = tree.insert(child13_6, "end", text="Shoes")
    child13_6_6 = tree.insert(child13_6, "end", text="Shops")
    child13_6_7 = tree.insert(child13_6, "end", text="Watches")
    
    child13_7 = tree.insert(parent_item13, "end", text="Novelty & More")
    child13_8 = tree.insert(parent_item13, "end", text="Shoe, Jewelry & Watch Accessories")
    child13_9 = tree.insert(parent_item13, "end", text="Sport Specific Clothing")
    child13_10 = tree.insert(parent_item13, "end", text="Uniforms, Work & Safety")
    child13_11 = tree.insert(parent_item13, "end", text="Women")

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
    child22_1 = tree.insert(parent_item22, "end", text="Beauty & Grooming")
    child22_2 = tree.insert(parent_item22, "end", text="Clothing, Shoes & Accessories")
    child22_3 = tree.insert(parent_item22, "end", text="Electronics Accessories")
    child22_4 = tree.insert(parent_item22, "end", text="Health & Personal Care")
    child22_5 = tree.insert(parent_item22, "end", text="Home & Kitchen")
    child22_6 = tree.insert(parent_item22, "end", text="Jewelry")
    child22_7 = tree.insert(parent_item22, "end", text="Pet Supplies")
    child22_8 = tree.insert(parent_item22, "end", text="Sports & Outdoors")
    child22_9 = tree.insert(parent_item22, "end", text="Stationery & Party Supplies")
    child22_10 = tree.insert(parent_item22, "end", text="Toys & Games")

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

    tree.bind("<<TreeviewSelect>>", on_select)
    
    
    # tree.tag_bind("link", "<Button-1>", on_select)

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
        image=start_img, borderwidth=0, highlightthickness=0, relief="flat",command=lambda : scrape_site(), activebackground= "#202020")
    start_btn.place(x=75, y=720, width=100, height=47)

    stop_img = PhotoImage(file=relative_to_assets("stop.png"))    
    stop_btn = Button(image=stop_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
    stop_btn.place(x=325, y=720, width=100, height=47)

    Display_img = PhotoImage(file=relative_to_assets("result.png"))    
    Display_btn = Button(image=Display_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
    Display_btn.place(x=575, y=720, width=100, height=47)

    Import_img = PhotoImage(file=relative_to_assets("import.png"))    
    Import_btn = Button(image=Import_img, borderwidth=0, highlightthickness=0, relief="flat",activebackground= "#202020")
    Import_btn.place(x=825, y=720, width=100, height=47)
    
    window.resizable(False, False)
    # Run the main event loop to display the window
    window.mainloop()
BuildingGUI()


        