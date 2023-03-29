"""Tests for the data collection."""

import numpy as np
import pandas as pd
import pytest
import houseprice.data_collection.util_collect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from houseprice.data_collection.util_collect import get_num_page
from houseprice.data_collection.util_collect import get_attr_info
from houseprice.data_collection.util_collect import get_main_info
from houseprice.data_collection.util_collect import collect_attr
from houseprice.data_collection.util_collect import collect_data
from houseprice.data_collection.util_collect import get_to_page
from houseprice.data_collection.util_collect import get_page_ads



@pytest.fixture()
def url():
    return "https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/"


# def test_fit_logit_model_error_model_type(data, data_info):
#     with pytest.raises(ValueError):  # noqa: PT011
#         assert fit_logit_model(data, data_info, model_type="quadratic")


@pytest.fixture(scope="session")
def driver():
    # Assuming you have Chrome installed in the default location
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(chrome_options=chrome_options)
    yield driver
    driver.quit()

def test_get_num_page(driver):
    driver.get("https://example.com")  # Replace with the URL of the website you want to test
    num_pages = get_num_page(driver)
    assert isinstance(num_pages, int)  # Make sure the function returns an integer
    assert num_pages > 0  # Make sure the number of pages is positive


@pytest.fixture(scope="module")
def driver():
    """Create a WebDriver object for testing."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_driver_page(driver):
    url = "https://www.unegui.mn/"
    driver.get(url)
    assert driver.current_url.startswith(url)


def test_get_attr_info(driver):
    """Test the get_attr_info function."""
    # Load the test page
    driver.get("https://example.com/test-page")

    # Mock the result of the XPATH selectors
    flag_3_element = driver.find_element(By.XPATH, "//*[@id='show-post-render-app']/div/section[1]/div/div[2]/div[1]/div[3]/ul/li[1]")
    flag_3_element.text = "Attribute 1: Value 1\nAttribute 2: Value 2\nAttribute 3: Value 3"

    # Call the function and assert the result
    expected_result = [('Attribute 1', 'Value 1'), ('Attribute 2', 'Value 2'), ('Attribute 3', 'Value 3')]
    assert get_attr_info(driver) == expected_result


@pytest.fixture
def driver():
    # Set up the Selenium WebDriver object
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.example.com')
    yield driver
    driver.quit()

def test_get_main_info(driver):
    # Navigate to the ad page
    driver.get('https://www.example.com/ad/1234')

    # Call the function to extract the main information
    result = get_main_info(driver)

    # Check that the title and price information is correct
    assert result['Title'] == 'Example Ad'
    assert result['Price'] == '$100'


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.get('https://example.com')
    yield driver
    driver.quit()


def test_collect_attr(driver):
    attr = driver.find_elements(By.XPATH, "//div[@class='attributes']/ul/li")
    d = {"Title": "Example Title", "Price": "$99.99"}
    d = collect_attr(driver, attr, d)
    expected = {"Title": "Example Title", "Price": "$99.99", "Attribute1": "Value1", "Attribute2": "Value2"}
    assert isinstance(d, dict)
    assert all(item in expected.items() for item in d.items())


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def ad_element(driver):
    driver.get("https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/")
    ad_element = driver.find_element(By.XPATH, "//div[@class='ad']")
    yield ad_element

def test_collect_data(driver, ad_element):
    data = collect_data(driver, ad_element)
    assert "Title" in data
    assert "Price" in data
    assert "Attribute1" in data
    assert "Attribute2" in data


def test_get_to_page(driver):
    url = "https://example.com/ads"
    page = 3
    driver = get_to_page(driver, url, page)
    assert driver.current_url == f"{url}?page={page}"


def test_get_page_ads(driver):
    # Test that the function returns a list of ads when there are ads on the page.
    driver.get('https://example.com/ads?page=1')
    ads = get_page_ads(driver)
    assert type(ads) == list

def test_get_page_ads_no_ads(driver):
    # Test that the function returns None when there are no ads on the page.
    driver.get('https://example.com/ads?page=2')
    ads = get_page_ads(driver)
    assert ads == []

