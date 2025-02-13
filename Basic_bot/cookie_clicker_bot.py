#cookie clicker bot

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
url = r'https://orteil.dashnet.org/cookieclicker/'

driver.get(url)
cookie_id = 'bigCookie'
product_price_prefix = "productPrice"
product_prefix = "product"


WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'english')]"))
)

language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
language.click()

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, cookie_id))
)

cookie_clicker = driver.find_element(By.ID, cookie_id)


while True:
    cookie_clicker.click()
    cookie_count = driver.find_element(By.ID, 'cookies').text.split(" ")[0]
    cookie_count = int(cookie_count.replace(',',''))
    if cookie_count % 100 == 0:
        print(cookie_count)
    for i in range(4):
        product_price = driver.find_element(By.ID, product_price_prefix + str(i)).text.replace(',','')
        if not product_price.isdigit():
            continue
        product_price = int(product_price)
        
        if cookie_count >= product_price:
            product = driver.find_element(By.ID, product_prefix + str(i))
            product.click()
            break
        
        
    
    
    
time.sleep(100)
driver.quit()

