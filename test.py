from selenium import webdriver

# Create a ChromeOptions instance
options = webdriver.ChromeOptions()

# Replace this with the actual path to your Chrome user profile directory
options.add_argument("user-data-dir=C:\\Users\\JSGURU\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 9")

# Disable the "DevToolsActivePort" check, as it can sometimes cause issues
options.add_argument("--disable-dev-shm-usage")

# Disable the "sandbox" mode if you encounter issues
options.add_argument("--no-sandbox")

# Create a Chrome webdriver instance with the options
driver = webdriver.Chrome(options=options)

# Open a website
driver.get("https://google.com")

while True:
    pass