import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def save_data(data):
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    # Save the DataFrame to a CSV file with UTF-8 encoding
    df.to_csv("output1.csv", index=False, encoding="utf-8-sig")

def run_collection():
    chrome_options = Options() # Initialize options for Chrome browser
    driver = webdriver.Chrome(options=chrome_options) # New webdriver instance

    # Navigate to ads page for Ulaanbaatar flats
    driver.get("https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/")

    # Find the number of pages to go through
    num_pages = int(driver.find_element(By.XPATH,"//*[@id='listing']/section/div[2]/div[1]/div[2]/ul[@class='number-list']/li[8]/a").text)


    ### MAIN PART

    # Create an empty list to store the data
    data = []
    # Loop through all the pages and scrape the data
    for page in range(1, num_pages + 1):
        # Navigate to the page
        if page > 1:
            driver.get(f"https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/?page={page}")

        # Find all elements on the page that match the specified XPath.
        try:
            listings = driver.find_elements(By.XPATH,"//*[@id='listing']/section/div[2]/div[1]/div[2]/ul[1]/li")
        except NoSuchElementException:
            continue


        # Loop through each listing on the page
        for listing in listings:

            # Click on the listing to view its details
            listing.find_element(By.XPATH, "a").click()

            # Get the attributes, title, price, and description
            check3 = driver.find_elements(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[3]/ul/li")
            check4 = driver.find_elements(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[4]/ul/li")
            check5 = driver.find_elements(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[5]/ul/li")

            if len(check3) > 10:
                attr = check3
            elif len(check4) > 10:
                attr = check4
            else:
                attr = check5

            title = driver.find_element(By.XPATH, "//*[@id='ad-title']").text
            try:
                price = driver.find_element(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[3]/div/div[1]/div[1]/div/div")
                price = price.text
            except NoSuchElementException:
                price = None

            # Create a dictionary with the data
            d = {"Title": title, "Price": price}

            # loop through attributes and collect
            for a in attr:
                try:
                    key = a.find_element(By.XPATH, "span[1]").text
                except NoSuchElementException:
                    key = None
                try:
                    value = a.find_element(By.XPATH, "span[2]").text
                except NoSuchElementException:
                    value = a.find_element(By.XPATH, "a").text
                d[key] = value

            # Add the dictionary to the data list
            data.append(d)

            # Go back to the list of listings
            driver.back()

    save_data(data)
