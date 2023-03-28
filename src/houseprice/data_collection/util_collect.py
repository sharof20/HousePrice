import pandas as pd
import pdb
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_collection(url):
    driver = driver_page(url)
    num_page = get_num_page(driver) # number of pages with ads
    data = []
    for page in range(1, num_page + 1): #
        driver   = get_to_page(driver, url, page)
        page_ads = get_page_ads(driver)
        for ad in page_ads:
            d = collect_data(driver, ad)
            data.append(d)
            driver.back()

    driver.quit()
    return data


def driver_page(url):
    chrome_options = Options() # Initialize options for Chrome browser
    driver = webdriver.Chrome(options=chrome_options) # New webdriver instance

    # Navigate to ads page for Ulaanbaatar flats
    driver.get(url)

    return driver

def get_num_page(driver):
    num_pages = int(driver.find_element(By.XPATH,"//*[@id='listing']/section/div[2]/div[1]/div[2]/ul[@class='number-list']/li[8]/a").text)
    return num_pages

def get_attr_info(driver):
    # Depending on the ad content, it is either div[3], div[4] or div[5]
    flag_3 = driver.find_elements(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[3]/ul/li")
    flag_4 = driver.find_elements(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[4]/ul/li")
    flag_5 = driver.find_elements(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[5]/ul/li")

    if len(flag_3) > 10:
        attr = flag_3
    elif len(flag_4) > 10:
        attr = flag_4
    else:
        attr = flag_5

    return attr

def get_main_info(driver):
    title = driver.find_element(By.XPATH, "//*[@id='ad-title']").text
    try:
        price = driver.find_element(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[3]/div/div[1]/div[1]/div/div")
        price = price.text
    except NoSuchElementException:
        price = None

    # Create a dictionary with the data
    d = {"Title": title, "Price": price}

    return d

def collect_attr(driver, attr, d):
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

    return d

def collect_data(driver, ad):
    ad.find_element(By.XPATH, "a").click()
    # get title and price of ad
    d = get_main_info(driver)

    # Get the attributes, title, price, and description
    attr = get_attr_info(driver)

    # loop through attributes and collect
    d = collect_attr(driver, attr, d)

    return d

def get_to_page(driver, url, page):
    driver.get(url + f"?page={page}")
    return driver

def get_page_ads(driver):
    # Find all elements on the page that match the specified XPath.
    try:
        page_ads = driver.find_elements(By.XPATH,"//*[@id='listing']/section/div[2]/div[1]/div[2]/ul[1]/li")
    except NoSuchElementException:
        page_ads = None

    return page_ads