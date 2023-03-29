import pandas as pd
import pdb
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def run_collection(url):
    """Scrape data from a web page with ads using Selenium.

    Parameters:
        url (str): The URL of the web page with ads to be scraped.

    Returns:
        list: A list of dictionaries containing the scraped data from each ad on the web page.

    Selenium is used to automate the process of web scraping:

    - driver_page(url): Returns a new Selenium WebDriver object for the given URL.
    - get_num_page(driver): Given a Selenium WebDriver object, returns the number of pages of ads.
    - get_to_page(driver, url, page): Given a Selenium WebDriver object, a URL, and a page number, navigates to the specified page of ads.
    - get_page_ads(driver): Given a Selenium WebDriver object, returns a list of web elements containing ads.
    - collect_data(driver, ad): Given a Selenium WebDriver object and a web element containing an ad, scrapes the data from the ad and returns it as a dictionary.

    The run_collection function works as follows:

    1. A new Selenium WebDriver object is created using the driver_page helper function.
    2. The number of pages with ads on the web page is determined using the get_num_page helper function.
    3. An empty list is created to store the scraped data.
    4. For each page of ads on the web page:
        - The Selenium WebDriver object is navigated to the current page of ads using the get_to_page helper function.
        - A list of web elements containing ads is obtained using the get_page_ads helper function.
        - For each ad on the page of ads:
            - The data from the ad is scraped and stored as a dictionary using the collect_data helper function.
            - The dictionary is appended to the list of scraped data.
            - The Selenium WebDriver object is navigated back to the previous page.
    5. The Selenium WebDriver object is closed.
    6. The list of scraped data is returned.

    """
    # implementation of the function
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
    """Initialize and return a new Selenium WebDriver object for the given URL using
    Google Chrome browser.

    Parameters:
        url (str): The URL of the web page to be loaded in the Chrome browser.

    Returns:
        selenium.webdriver.chrome.webdriver.WebDriver: A new Selenium WebDriver object for the given URL.

    The function initializes a new instance of the Google Chrome browser using the webdriver.Chrome function from the
    Selenium library. It then loads the specified URL using the driver.get method and returns the resulting
    Selenium WebDriver object. Chrome options can be customized by modifying the chrome_options variable.

    """
    # implementation of the function
    chrome_options = Options() # Initialize options for Chrome browser
    driver = webdriver.Chrome(options=chrome_options) # New webdriver instance

    # Navigate to ads page for Ulaanbaatar flats
    driver.get(url)

    return driver

def get_num_page(driver):
    """Return the total number of pages with ads from the given WebDriver object.

    Parameters:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): A Selenium WebDriver object representing the
        current state of the web page.

    Returns:
        int: The total number of pages with ads as an integer.

    The function extracts the total number of pages with ads from the given WebDriver object by selecting the 8th
    list item in the number list using an XPATH selector. The XPATH selector may need to be modified if the HTML
    structure of the web page changes.

    """
    # implementation of the function
    num_pages = int(driver.find_element(By.XPATH,"//*[@id='listing']/section/div[2]/div[1]/div[2]/ul[@class='number-list']/li[8]/a").text)
    return num_pages

def get_attr_info(driver):
    """Extract and return the attributes information for a given ad from the given
    WebDriver object.

    Parameters:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): A Selenium WebDriver object representing the
        current state of the web page.

    Returns:
        list: A list of attributes for the ad, where each attribute is represented as a key-value pair in the format
        ('attribute name', 'attribute value').

    The function extracts the attributes information for a given ad from the given WebDriver object. It returns a
    list of key-value pairs that represent each attribute of the ad. The function uses XPATH selectors to locate
    the <div> element that contains the attribute information and then parses the information into a list.

    """
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
    """Extract and return the main information for a given ad from the given WebDriver
    object.

    Parameters:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): A Selenium WebDriver object representing the
        current state of the web page.

    Returns:
        dict: A dictionary containing the title and price information for the ad.

    The function extracts the title and price information for a given ad from the given WebDriver object. It returns
    a dictionary containing the extracted information.

    """
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
    """Collects attribute data from a given ad and stores it in a dictionary.

    Parameters:
    driver (webdriver.Chrome): The Selenium webdriver instance for the current session.
    attr (list): A list of web elements containing the attribute information for a single ad.
    d (dict): A dictionary containing the ad's main information.

    Returns:
    dict: A dictionary containing the ad's main information and its attribute data.

    """
    # loop through attributes and collect
    for a in attr:
        # Try to extract the attribute key
        try:
            key = a.find_element(By.XPATH, "span[1]").text
        except NoSuchElementException:
            key = None
        # Try to extract the attribute value
        try:
            value = a.find_element(By.XPATH, "span[2]").text
        except NoSuchElementException:
            value = a.find_element(By.XPATH, "a").text
        d[key] = value

    return d

def collect_data(driver, ad):
    """Collects data for a given ad by clicking on its link and gathering its
    attributes, title, price, and description. Returns a dictionary with the collected
    data.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        ad (WebElement): The WebElement object that represents the ad.

    Returns:
        dict: A dictionary containing the collected data for the ad, with keys for "Title", "Price", and other attribute names.

    """
    ad.find_element(By.XPATH, "a").click()
    # get title and price of ad
    d = get_main_info(driver)

    # Get the attributes, title, price, and description
    attr = get_attr_info(driver)

    # loop through attributes and collect
    d = collect_attr(driver, attr, d)

    return d

def get_to_page(driver, url, page):
    """Navigate to a specific page of the ads page by modifying the URL with the given
    page number.

    Args:
    - driver: WebDriver instance
    - url: str, the base URL of the ads page
    - page: int, the page number to navigate to

    Returns:
    - driver: WebDriver instance, the driver instance after navigating to the desired page

    """
    driver.get(url + f"?page={page}")
    return driver


def get_page_ads(driver):
    """Get ads on the current page.

    Args:
        driver (webdriver.Chrome): The webdriver instance.
    Returns:
        list: List of all ad elements on the current page. Returns None if no ads are found.

    """
    # Find all elements on the page that match the specified XPath.
    try:
        page_ads = driver.find_elements(By.XPATH,"//*[@id='listing']/section/div[2]/div[1]/div[2]/ul[1]/li")
    except NoSuchElementException:
        page_ads = None

    return page_ads
