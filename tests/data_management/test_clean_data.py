import re
import numpy as np
import pandas as pd
import pytest
from houseprice.config import TEST_DIR
from houseprice.data_management import clean_data

from houseprice.data_management.clean_data import transliterate_mn
from houseprice.data_management.clean_data import extract_currency_value
from houseprice.data_management.clean_data import remove_location_and_code_columns
from houseprice.data_management.clean_data import extract_numeric_area_values
from houseprice.data_management.clean_data import change_column_data_type_to_string
from houseprice.data_management.clean_data import replace_no_balcony_with_zero
from houseprice.data_management.clean_data import translate_mongolian_flooring_material_types_to_english
from houseprice.data_management.clean_data import translate_garage_status_to_binary
from houseprice.data_management.clean_data import translate_mongolian_window_types_to_english
from houseprice.data_management.clean_data import translate_mongolian_door_types_to_english
from houseprice.data_management.clean_data import translate_mongolian_lease_types_to_english
from houseprice.data_management.clean_data import parse_balcony_numbers_from_column
from houseprice.data_management.clean_data import translate_mongolian_colnames_to_english
from houseprice.data_management.clean_data import filter_dataframe_by_column_range

#transliterate_mn
#extract_price
#drop_columns
#rename_columns
#extract_and_convert_area
#convert_column_to_string
#replace_balcony_no
#extract_balcony_numbers
#filter_by_range
#replace_flooring_material
#replace_garage
#replace_window_type
#replace_door_type
#replace_lease_type
#clean_manual



def test_transliterate_mn():
    assert transliterate_mn('Монгол бичиг') == 'Mongol bichig'
    assert transliterate_mn('Би хоол хиймээ гэж бодож байна') == 'Bi khool khiimee gej bodoj baina'


@pytest.fixture
def test_data():
    data = {
        "location:": ['Ulaanbaatar', 'Erdenet', 'Darkhan'],
        "Код:": [1, 2, 3],
        "Title": ['Apartment 1', 'Apartment 2', 'Apartment 3'],
        "price": ['10 сая ₮', '20 сая ₮', '30 сая ₮'],
        "number_of_balcony": ["1 Tarтrүй", "2", "Tarтrүй"],
        "area_sq_m": ["100.5 sq m", "75 sq m", "85.2 sq m"],
        "flooring_material": ["Паркет", "Ламинат", "Цемент"],
        "garage": ["Байгаа", "Байгаа", "Байхгүй"],
        "window_type": ["Вакум", "Модон вакум", "Мод"],
        "door_type": ["Бүргэд", "Төмөр", "Вакум"],
        "leasing": ["Банкны лизингтэй", "Лизинггүй", "Хувь лизингтэй"]
    }
    return pd.DataFrame(data)


def test_extract_currency_value():
    # Test the function with valid input
    assert extract_currency_value('10 сая ₮') == 10.0
    assert extract_currency_value('20 сая ₮') == 20.0
    assert extract_currency_value('30 сая ₮') == 30.0

    # Test the function with invalid input
    with pytest.raises(IndexError):
        extract_currency_value('бум сая ₮')

def test_extract_currency_value_with_dataframe(test_data):
    # Test the function with a pandas DataFrame
    test_data['price'] = test_data['price'].apply(extract_currency_value)
    assert test_data['price'].equals(pd.Series([10.0, 20.0, 30.0]))


def test_remove_location_and_code_columns(test_data):
    # Ensure that the returned dataframe has the specified columns dropped
    result = remove_location_and_code_columns(test_data)
    assert "location:" not in result.columns
    assert "Код:" not in result.columns

    # Ensure that the original dataframe is not modified
    assert "location:" in test_data.columns
    assert "Код:" in test_data.columns


def test_extract_numeric_area_values(test_data):
    result = extract_numeric_area_values(test_data)
    expected_area = pd.Series([100.5, 75, 85.2], name="area_sq_m")
    assert np.allclose(result["area_sq_m"], expected_area)


def test_change_column_data_type_to_string(test_data):
    # Test if the function returns a DataFrame
    assert isinstance(change_column_data_type_to_string(test_data, 'Title'), pd.DataFrame)

    # Test if the column type is changed to string
    assert change_column_data_type_to_string(test_data, 'Title')['Title'].dtype == 'object'

    # Test if the values in the column are all strings
    assert all(isinstance(val, str) for val in change_column_data_type_to_string(test_data, 'Title')['Title'].values)

    # Test if the function raises an error if the column name is not in the DataFrame
    with pytest.raises(KeyError):
        change_column_data_type_to_string(test_data, 'Non-existent column')


def test_replace_no_balcony_with_zero(test_data):
    # Call the function with test data
    result = replace_no_balcony_with_zero(test_data)

    # Check that the original column is of string type
    assert result["number_of_balcony"].dtype == "object"

    # Check that "Tarтrүй" is replaced with "0 Tarтrүй"
    assert result["number_of_balcony"].iloc[2] == "0 Tarтrүй"


def test_translate_mongolian_flooring_material_types_to_english(test_data):
    # call the function with the test data
    result = translate_mongolian_flooring_material_types_to_english(test_data)

    # define the expected output
    expected_output = {
        "location:": ['Ulaanbaatar', 'Erdenet', 'Darkhan'],
        "Код:": [1, 2, 3],
        "Title": ['Apartment 1', 'Apartment 2', 'Apartment 3'],
        "price": ['10 сая ₮', '20 сая ₮', '30 сая ₮'],
        "number_of_balcony": ["1 Tarтrүй", "2", "Tarтrүй"],
        "area_sq_m": ["100.5 sq m", "75 sq m", "85.2 sq m"],
        "flooring_material": ["parquet", "laminate", "cement"],
        "garage": ["Байгаа", "Байгаа", "Байхгүй"],
        "window_type": ["Вакум", "Модон вакум", "Мод"],
        "door_type": ["Бүргэд", "Төмөр", "Вакум"],
        "leasing": ["Банкны лизингтэй", "Лизинггүй", "Хувь лизингтэй"]
    }
    expected_output = pd.DataFrame(expected_output)

    # check that the output matches the expected output
    pd.testing.assert_frame_equal(result, expected_output)


def test_translate_garage_status_to_binary(test_data):
    expected = pd.DataFrame({
        "location:": ['Ulaanbaatar', 'Erdenet', 'Darkhan'],
        "Код:": [1, 2, 3],
        "Title": ['Apartment 1', 'Apartment 2', 'Apartment 3'],
        "price": ['10 сая ₮', '20 сая ₮', '30 сая ₮'],
        "number_of_balcony": ["1 Tarтrүй", "2", "Tarтrүй"],
        "area_sq_m": ["100.5 sq m", "75 sq m", "85.2 sq m"],
        "flooring_material": ["Паркет", "Ламинат", "Цемент"],
        "garage": ["yes", "yes", "no"],
        "window_type": ["Вакум", "Модон вакум", "Мод"],
        "door_type": ["Бүргэд", "Төмөр", "Вакум"],
        "leasing": ["Банкны лизингтэй", "Лизинггүй", "Хувь лизингтэй"]
    })
    result = translate_garage_status_to_binary(test_data)
    pd.testing.assert_frame_equal(result, expected)


def test_translate_mongolian_window_types_to_english(test_data):
    # Define the expected output
    expected_output = pd.DataFrame({
        "location:": ['Ulaanbaatar', 'Erdenet', 'Darkhan'],
        "Код:": [1, 2, 3],
        "Title": ['Apartment 1', 'Apartment 2', 'Apartment 3'],
        "price": ['10 сая ₮', '20 сая ₮', '30 сая ₮'],
        "number_of_balcony": ["1 Tarтrүй", "2", "Tarтrүй"],
        "area_sq_m": ["100.5 sq m", "75 sq m", "85.2 sq m"],
        "flooring_material": ["Паркет", "Ламинат", "Цемент"],
        "garage": ["Байгаа", "Байгаа", "Байхгүй"],
        "window_type": ["vinyl", "vinwood", "wood"],
        "door_type": ["Бүргэд", "Төмөр", "Вакум"],
        "leasing": ["Банкны лизингтэй", "Лизинггүй", "Хувь лизингтэй"]
    })

    # Call the function with the test data
    result = translate_mongolian_window_types_to_english(test_data)

    # Compare the result with the expected output
    pd.testing.assert_frame_equal(result, expected_output)


def test_translate_mongolian_door_types_to_english(test_data):
    # Replace Mongolian Cyrillic door types with their English equivalents
    result = translate_mongolian_door_types_to_english(test_data)

    # Define the expected output DataFrame
    expected_output = pd.DataFrame({
        "location:": ['Ulaanbaatar', 'Erdenet', 'Darkhan'],
        "Код:": [1, 2, 3],
        "Title": ['Apartment 1', 'Apartment 2', 'Apartment 3'],
        "price": ['10 сая ₮', '20 сая ₮', '30 сая ₮'],
        "number_of_balcony": ["1 Tarтrүй", "2", "Tarтrүй"],
        "area_sq_m": ["100.5 sq m", "75 sq m", "85.2 sq m"],
        "flooring_material": ["Паркет", "Ламинат", "Цемент"],
        "garage": ["Байгаа", "Байгаа", "Байхгүй"],
        "window_type": ["Вакум", "Модон вакум", "Мод"],
        "door_type": ["burged", "iron", "vacuum"],
        "leasing": ["Банкны лизингтэй", "Лизинггүй", "Хувь лизингтэй"]
    })

    # Compare the result with the expected output
    assert result.equals(expected_output)


def test_translate_mongolian_lease_types_to_english(test_data):
    expected_output = {
        "location:": ['Ulaanbaatar', 'Erdenet', 'Darkhan'],
        "Код:": [1, 2, 3],
        "Title": ['Apartment 1', 'Apartment 2', 'Apartment 3'],
        "price": ['10 сая ₮', '20 сая ₮', '30 сая ₮'],
        "number_of_balcony": ["1 Tarтrүй", "2", "Tarтrүй"],
        "area_sq_m": ["100.5 sq m", "75 sq m", "85.2 sq m"],
        "flooring_material": ["Паркет", "Ламинат", "Цемент"],
        "garage": ["Байгаа", "Байгаа", "Байхгүй"],
        "window_type": ["Вакум", "Модон вакум", "Мод"],
        "door_type": ["Бүргэд", "Төмөр", "Вакум"],
        "leasing": ['withlease', 'nolease', 'privlease']
    }

    result = translate_mongolian_lease_types_to_english(test_data)

    assert result.equals(pd.DataFrame(expected_output))


@pytest.fixture
def test_data_2():
    data = {
        "location:": ['Ulaanbaatar', 'Erdenet', 'Darkhan'],
        "Kod:": [1, 2, 3],
        "Title": ['Apartment 1', 'Apartment 2', 'Apartment 3'],
        "number_of_balcony": ['1 balcony', '2.5 balconies', 'No balcony'],
        "area_sq_m": ["100.5 sq m", "75 sq m", "85.2 sq m"]
    }
    return pd.DataFrame(data)

def test_parse_balcony_numbers_from_column(test_data_2):
    expected_output = pd.DataFrame({
        "location:": ['Ulaanbaatar', 'Erdenet', 'Darkhan'],
        "Kod:": [1, 2, 3],
        "Title": ['Apartment 1', 'Apartment 2', 'Apartment 3'],
        "number_of_balcony": [1.0, 2.5, np.nan],
        "area_sq_m": ["100.5 sq m", "75 sq m", "85.2 sq m"]
    })

    # Ensure that the function returns the expected output
    assert parse_balcony_numbers_from_column(test_data_2).equals(expected_output)


@pytest.fixture
def test_data_3():
    data = {"price": [50000, 75000, 100000, 150000]}
    return pd.DataFrame(data)

def test_filter_dataframe_by_column_range(test_data_3):
    # Arrange
    column_name = "price"
    min_value = 75000
    max_value = 150000
    expected_output = pd.DataFrame({"price": [75000, 100000, 150000]}).reset_index(drop=True)

    # Act
    filtered_df = filter_dataframe_by_column_range(test_data_3, column_name, min_value, max_value).reset_index(drop=True)

    # Assert
    assert filtered_df.equals(expected_output)



@pytest.fixture
def sample_df():
    data = {
        'Title': ['Beautiful house in the city center', 'Spacious apartment with balcony'],
        'Price': ['₮400,000,000', '₮150,000,000'],
        'Шал:': ['Wooden', 'Parquet'],
        'Тагт:': [1, 2],
        'Ашиглалтанд орсон он:': [2010, 2015],
        'Гараж:': ['Yes', 'No'],
        'Цонх:': ['Plastic', 'Metal'],
        'Барилгын давхар:': [2, 4],
        'Хаалга:': ['Wooden', 'Metal'],
        'Талбай:': [200, 100],
        'Хэдэн давхарт:': [1, 3],
        'Лизингээр авах боломж:': ['Yes', 'No'],
        'Дүүрэг:': ['Sukhbaatar', 'Bayangol'],
        'Цонхны тоо:': [4, 6],
        'Байршил:': ['Ulaanbaatar', 'Darkhan'],
        'Барилгын явц:': ['Finished', 'In progress']
    }
    return pd.DataFrame(data)

def test_translate_mongolian_colnames_to_english(sample_df):
    expected_df = pd.DataFrame({
        'title': ['Beautiful house in the city center', 'Spacious apartment with balcony'],
        'price_text': ['₮400,000,000', '₮150,000,000'],
        'flooring_material': ['Wooden', 'Parquet'],
        'number_of_balcony': [1, 2],
        'year_of_commissioning': [2010, 2015],
        'garage': ['Yes', 'No'],
        'window_type': ['Plastic', 'Metal'],
        'number_of_storeys': [2, 4],
        'door_type': ['Wooden', 'Metal'],
        'area_sq_m': [200, 100],
        'apartment_storey': [1, 3],
        'leasing': ['Yes', 'No'],
        'district': ['Sukhbaatar', 'Bayangol'],
        'number_of_windows': [4, 6],
        'location': ['Ulaanbaatar', 'Darkhan'],
        'construction_progress': ['Finished', 'In progress']
    })

    assert translate_mongolian_colnames_to_english(sample_df).equals(expected_df)





