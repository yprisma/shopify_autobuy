from time import sleep
from urllib.request import Request, urlopen
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import http.client, urllib
from pushoverSecrets import user, token
from selenium import webdriver
import pickle
import datetime
from random import randrange

# load cookies for login
def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)

# make a post request to send a message
def ping():
    # Grab pushover API
    conn = http.client.HTTPSConnection("api.pushover.net:443") # Create a connection to the API
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": token,
        "user": user,
        "message": "Formd T1 is in-stock! Check if bot worked!",
    }), { "Content-type": "application/x-www-form-urlencoded" })

# set bought status and open chrome, load the webpage and refresh to restore account via cookies
bought = False
driver = webdriver.Chrome()
driver.get('https://formdt1.com/products/t1titanium?variant=47314104058174')
load_cookie(driver, '/path/to/cookie')

# indefinite loop to check if shoppay button is active
# if it is, will purchase and send ping to phone
while not bought:
    driver.refresh()
    element = driver.find_element(By.XPATH, '//*[@id="product-form-template--23512636916030__main"]/div/div/shopify-accelerated-checkout/shop-pay-wallet-button')
    try:
        if element.get_attribute('disabled'): # check if button has disabled field
            # Get the current date and time
            now = datetime.datetime.now()
            print(now.strftime("%Y-%m-%d %H:%M:%S") + ' Not available, refreshing page')
            # driver.refresh()
        else:
            print('GOGOGOGOGO!!!!!')
            element.click()
            pay_button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div[1]/div/div[1]/div/main/div/form/div[1]/div[2]/div/div/div/section/div[2]/div[2]/div/div/div/div/div/button')
            pay_button.click()
            bought = True
            ping()
    except KeyboardInterrupt:
        sys.exit()
        # print('Something went wrong')
        # pass
    sleep(randrange(1800, 2300)) # Do this function every hour in practice, for testing do seconds


# test ping
conn = http.client.HTTPSConnection("api.pushover.net:443") # Create a connection to the API

conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": token,
        "user": user,
        "message": "Formd T1 is in-stock! Check if bot worked!",
    }), { "Content-type": "application/x-www-form-urlencoded" })