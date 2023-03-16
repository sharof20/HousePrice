import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Initialize options for Chrome browser
chrome_options = Options()

# Create a new WebDriver instance with Chrome browser and set options
driver = webdriver.Chrome(options=chrome_options)


# This navigates the browser instance to the URL specified
driver.get("https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/")

# Find all elements on the page that match the specified XPath.
listing = driver.find_elements(
    By.XPATH,
    "//*[@id='listing']/section/div[2]/div[1]/div[2]/ul/li",
)

# Find the number of web-pages available
num_pages = int(
    driver.find_element(
        By.XPATH,
        "//*[@id='listing']/section/div[2]/div[1]/div[2]/ul[@class='number-list']/li[8]/a",
    ).text,
)

# Create an empty list to store the prices.
price_list = []


listing[0].find_element(By.XPATH, "a").click() # ("Энrийн зap", not promoted ones)

# list of attributes
attr = driver.find_elements(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[5]/ul/li")

# first attribute's key and value
key   = attr[0].find_element(By.XPATH, "span[1]").text
value = attr[0].find_element(By.XPATH, "span[2]").text

### title
title = driver.find_element(By.XPATH, "//*[@id='ad-title']").text

### price
price = driver.find_element(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[3]/div/div[1]/div[1]/div/div").text

### descriptions
desc = driver.find_element(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[6]/div").text

# go back to the list
driver.back()      # previous page in browser history


# Loop through all the pages and scrape the data
for page in range(1, num_pages + 1):
    # Navigate to the page
    if page > 1:
        driver.get(
            f"https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/?page={page}",
        )
        time.sleep(10)  # wait for the page to load

    # Find all elements on the page that match the specified XPath.
    try:
        listing = driver.find_elements(
            By.XPATH,
            "//*[@id='listing']/section/div[2]/div[1]/div[2]/ul/li",
        )
    except NoSuchElementException:
        continue

    # Iterate over the elements found in the previous step.
    for i in range(len(listing)):
        # Find the description, the number of rooms and price of each element using XPATH.
        try:
            desc = listing[i].find_element(By.XPATH, "div[1]/div[2]/div/a").text
        except NoSuchElementException:
            desc = ""
        try:
            price = listing[i].find_element(By.XPATH, "div[1]/div[3]/div").text
        except NoSuchElementException:
            price = ""
        try:
            room = (
                listing[i]
                .find_element(By.XPATH, "div[1]/div[2]/div/div[3]/span[2]")
                .text
            )
        except NoSuchElementException:
            room = ""
        # Append the description, price, and room to the price_list.
        price_list.append([desc, price, room])


# Create a pandas dataframe from the list of prices, with columns named "Taйл6ap" and "Yнэ".
df = pd.DataFrame(price_list, columns=["Taйл6ap", "Yнэ", "Opoo"])

# Save the dataframe to a CSV file named "unegui.csv", with UTF-8 encoding.
df.to_csv("unegui.csv", encoding="utf-8-sig")
