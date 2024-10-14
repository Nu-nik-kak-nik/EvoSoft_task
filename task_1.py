from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import csv
import time

driver = webdriver.Firefox()

driver.get("https://www.nseindia.com/")

market_data_element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//li/a[@title='Market Data']"))
)
ActionChains(driver).move_to_element(market_data_element).perform()

pre_open_market_element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//li/a[contains(text(), 'Pre-Open Market')]"))
)
pre_open_market_element.click()

time.sleep(5)

final_prices = []
final_price_elements = driver.find_elements(By.XPATH, "//td[contains(text(), 'Final Price')]")
for element in final_price_elements:
    final_prices.append(element.text.strip())

with open("pre_open_market_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Price"])
    for i, price in enumerate(final_prices):
        writer.writerow([f"Place {i + 1}", price])

driver.get("https://www.nseindia.com/")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

nifty_bank_element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//div[contains(text(), 'NIFTY BANK')]"))
)
nifty_bank_element.click()

view_all_element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//a[contains(text(), 'View all')]"))
)
view_all_element.click()

select_element = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((By.XPATH, "//select[@id='index-select']"))
)
select_element.click()
select_element.send_keys("NIFTY ALPHA 50")

driver.quit()