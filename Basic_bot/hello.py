from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
url = "https://www.selenium.dev/selenium/web/web-form.html"

driver.get(url)

title = driver.title
print(title)

driver.implicitly_wait(0.5)
time.sleep(5)

text_box = driver.find_element(by=By.NAME, value="my-text")
print(f"text_box: {text_box}")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
print(f"submit_button: {submit_button}")

text_box.send_keys("Selenium")
print(f"value: {text_box.get_attribute('value')}")
submit_button.click()


message = driver.find_element(by=By.ID, value="message")
print(message)
text = message.text

time.sleep(300)
driver.quit()



# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time

# # https://sites.google.com/chromium.org/driver/
# path_to_engine = r"C:/Choromium Engine/chromedriver-win64/chromedriver.exe"

# service = Service(executable_path=path_to_engine)
# driver = webdriver.Chrome(service=service)

# driver.get("https://www.google.com")

# WebDriverWait(driver,5).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, "gLFyf"))
# )

# search_box = driver.find_element(by=By.CLASS_NAME, value="gLFyf")
# search_box.clear()
# search_box.send_keys('tech with tim' + Keys.ENTER)
# print(f"search_box: {search_box}")

# #needs to get through recaptcha
# link = driver.find_element(By.PARTIAL_LINK_TEXT, "tech with tim")
# link.click()


# # select_element = driver.find_element(by=By.CLASS_NAME, value="VuuXrf")
# # select_element.send_keys('liquidpedia' + Keys.ENTER)


# time.sleep(100)
# driver.quit()