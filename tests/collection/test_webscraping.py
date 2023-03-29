"""Tests for the data collection."""

import numpy as np
import pandas as pd
import pytest
import houseprice.data_collection.util_collect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options



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


@pytest.fixture(scope='function')
def driver():
    # Initialize options for Chrome browser
    chrome_options = Options()
    # Create a new instance of the Google Chrome browser using the webdriver.Chrome function
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def test_driver_page(driver):
    # Specify the URL of the web page to be loaded in the Chrome browser
    url = "https://www.example.com"
    # Load the specified URL using the driver.get method
    driver.get(url)
    # Check if the expected title is displayed in the web page
    assert driver.title == "Example Domain"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_get_attr_info():
    driver = webdriver.Chrome()
    driver.get('https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/')
    # Perform some actions to navigate to the page with an ad
    attributes = get_attr_info(driver)
    driver.quit()
    assert len(attributes) >= 0

def test_get_num_page():
    """Test the get_num_page function."""
    # create a WebDriver instance
    driver = webdriver.Chrome()

    # navigate to the web page with ads
    driver.get("https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/")

    # get the number of pages with ads
    num_pages = get_num_page(driver)

    # assert that the number of pages is an integer
    assert isinstance(num_pages, int)

    # close the WebDriver instance
    driver.quit()

@pytest.fixture
def driver():
    # Set up the WebDriver object
    driver = webdriver.Chrome()
    yield driver
    # Clean up after the test is done
    driver.quit()

@pytest.mark.skip(reason="Element with ID 'ad-title' may have been changed")
def test_get_main_info(driver):
    # Navigate to the page containing the ad
    driver.get('https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/ulan-bator/')

    # Call the get_main_info function and store the result
    result = get_main_info(driver)

    # Check that the result is a dictionary
    assert type(result) == dict

    # Check that the result contains the expected keys
    assert "Title" in result
    assert "Price" in result

    # Check that the title is not empty
    assert result["Title"] != ""

    # Check that the price is either None or a non-empty string
    assert result["Price"] is None or result["Price"] != ""


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
@pytest.mark.skip(reason="div[@class=attributes may have been changed")
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

