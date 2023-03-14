import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Initialize options for Chrome browser
chrome_options = Options()

# Create a new WebDriver instance with Chrome browser and set options
driver = webdriver.Chrome(chrome_options=chrome_options)


# This navigates the browser instance to the URL specified
driver.get("https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/")

# This locates an element on the webpage using an XPath expression, then clicks on it.
# In this case, the element is located using the XPath //*[@id='trait_fields']/div[2]/div[2]/div[2].
driver.find_element(By.XPATH, "//*[@id='trait_fields']/div[2]/div[2]/div[2]").click()

# Find an element on the page using its XPath and click on it.
driver.find_element(
    By.XPATH,
    "//*[@id='trait_fields']/div[2]/div[2]/div[3]/ul[2]/li[19]/label",
).click()

# Wait for 10 seconds before continuing. This is not recommended as it blocks the program's execution.
time.sleep(10)

# Find an element on the page using its partial link text and click on it.
driver.find_element(By.PARTIAL_LINK_TEXT, "2 өpөө").click()

# Find all elements on the page that match the specified XPath.
listing = driver.find_elements(
    By.XPATH,
    "//*[@id='listing']/section/div[2]/div[1]/div[2]/ul/li",
)

# Create an empty list to store the prices.
price_list = []

# Iterate over the elements found in the previous step.
for i in range(len(listing)):
    # Find the description and price of each element using XPATH.
    desc = listing[i].find_element(By.XPATH, "div[1]/div[2]/div/a").text
    price = listing[i].find_element(By.XPATH, "div[1]/div[3]/div").text

    # Print the description and price to the console.

    # Append the description and price to the price_list.
    price_list.append([desc, price])

# Create a pandas dataframe from the list of prices, with columns named "Taйл6ap" and "Yнэ".
df = pd.DataFrame(price_list, columns=["Taйл6ap", "Yнэ"])

# Save the dataframe to a CSV file named "unegui1.csv", with UTF-8 encoding.
df.to_csv("unegui1.csv", encoding="utf-8-sig")
