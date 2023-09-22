from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

SCRAPEOPS_API_KEY = 'YOUR_API_KEY'

## Define ScrapeOps Proxy Port Endpoint
proxy_options = {
    'proxy': {
        'http': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'https': f'http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353',
        'no_proxy': 'localhost:127.0.0.1'
    }
}

## Set Up Selenium Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install(), 
                            seleniumwire_options=proxy_options)

## Send Request Using ScrapeOps Proxy
driver.get('http://quotes.toscrape.com/page/1/')

## Retrieve HTML Response
html_response = driver.page_source

## Extract Data From HTML
soup = BeautifulSoup(html_response, "html.parser")
h1_text = soup.find('h1').text

print(h1_text)