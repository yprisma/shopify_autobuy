import pickle
from selenium import webdriver

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
     with open(path, 'rb') as cookiesfile:
         cookies = pickle.load(cookiesfile)
         for cookie in cookies:
             driver.add_cookie(cookie)

driver = webdriver.Chrome()
driver.get('https://formdt1.com/products/t1epyc')

foo = input()

save_cookie(driver, '/path/to/file/cookie')