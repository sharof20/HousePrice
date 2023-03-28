"""Function(s) for cleaning the data set(s)."""
import pdb
from transliterate import translit
import re
import numpy as np
import pandas as pd


def clean_data(df):
    df = drop_columns(df)
    df = rename_columns(df)
    # extract numbers from the price column and convert to float
    df["price"] = df["price_text"].apply(extract_price)
    df = extract_and_convert_area(df)
    df = convert_column_to_string(df, "number_of_balcony")
    df = replace_balcony_no(df)
    df = extract_balcony_numbers(df)

    df = filter_by_range(df, "area_sq_m", 10, 1000)
    # Apply the function to the 'text' column
    df['location'] = df['location'].apply(transliterate_mn)
    df['district'] = df['district'].apply(transliterate_mn)
    df['title'] = df['title'].apply(transliterate_mn)
    df = replace_flooring_material(df)
    df = replace_garage(df)
    df = replace_window_type(df)
    df = replace_door_type(df)
    df = replace_lease_type(df)
    df = clean_manual(df)


    return df

# Define a function to transliterate Mongolian Cyrillic to English
def transliterate_mn(text):
    """Transliterates Mongolian Cyrillic text to English using the translit library.

    Args:
    - text (str): The input text in Mongolian Cyrillic to be transliterated.

    Returns:
    - str: The transliterated text in English.

    """
    return translit(text, 'mn', reversed=True)

def extract_price(x):
    """A function to extract the price from a string containing Mongolian currency
    notation.

    Args:
        x (str): A string containing the price in Mongolian currency notation.

    Returns:
        float: The extracted price as a float.

    Raises:
        IndexError: If no float number is found in the input string.

    """
    price = float(re.findall('(\\d+[\\.\\d]*)', x)[0])
    if 'бум' in x and 'сая' not in x:
        return price * 1e3
    else:
        return price

# drop_columns()
def drop_columns(df):
    """Drops the 'location:' and 'Koд:' columns from a DataFrame.

    Parameters:
    df (pandas DataFrame): The DataFrame from which to drop the columns.

    Returns:
    The modified DataFrame with the specified columns dropped.

    """
    return df.drop(["location:", "Код:"], axis=1)

# rename_columns()
def rename_columns(df):
    """Renames the columns of the given pandas DataFrame using a dictionary of old and
    new column names.

    Args:
    - df: a pandas DataFrame object

    Returns:
    - A pandas DataFrame object with the columns renamed according to the dictionary of old and new column names.

    """
    # create a dictionary of old and new column names
    new_names = {"Title": "title",
                "Price": "price_text",
                "Шал:": "flooring_material",
                "Тагт:": "number_of_balcony",
                "Ашиглалтанд орсон он:": "year_of_commissioning",
                "Гараж:": "garage",
                "Цонх:": "window_type",
                "Барилгын давхар:": "number_of_storeys",
                "Хаалга:": "door_type",
                "Талбай:": "area_sq_m",
                "Хэдэн давхарт:": "apartment_storey",
                "Лизингээр авах боломж:": "leasing",
                "Дүүрэг:": "district",
                "Цонхны тоо:": "number_of_windows",
                "Байршил:": "location",
                "Барилгын явц:": "construction_progress"}

    # rename the columns using the dictionary
    df = df.rename(columns=new_names)

    return df

# extract_and_convert_area()
def extract_and_convert_area(df):
    """Extracts numerical values from the 'area_sq_m' column of a given dataframe and
    converts them to floats.

    Parameters:
    df (pandas.DataFrame): A pandas dataframe containing an 'area_sq_m' column.

    Returns:
    pandas.DataFrame: A pandas dataframe with the 'area_sq_m' column updated to contain float values.

    """
    df["area_sq_m"] = df["area_sq_m"].str.extract("(\\d+[\\.\\d]*)").astype(float)
    return df

# convert_column_to_string()
def convert_column_to_string(df, column_name):
    """Convert a specified column in a pandas DataFrame to string type.

    Parameters:
        df (pandas DataFrame): The DataFrame containing the column to convert.
        column_name (str): The name of the column to convert to string type.

    Returns:
        The DataFrame with the specified column converted to string type.

    """
    df[column_name] = df[column_name].astype(str)
    return df

# replace_balcony_no()
def replace_balcony_no(df):
    """Replaces the string 'Tarтryй' in the 'number_of_balcony' column with '0 Tarтrүй'
    to indicate that there are no balconies.

    Args:
    df (pandas.DataFrame): The DataFrame containing the 'number_of_balcony' column.

    Returns:
    pandas.DataFrame: The DataFrame with the updated 'number_of_balcony' column.

    """
    # convert 'number_of_balcony:' column to string type before using .str accessor
    df["number_of_balcony"] = df["number_of_balcony"].astype(str)
    # replace 'Tarтryй', which means 'No balcony', with 0
    df["number_of_balcony"] = np.where(df["number_of_balcony"].str.contains("Tarтrүй"), "0 Tarтrүй", df["number_of_balcony"])
    return df

# extract_balcony_numbers()
def extract_balcony_numbers(df):
    """Extracts balcony numbers from the 'number_of_balcony' column in the input
    DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame containing a 'number_of_balcony' column.

    Returns:
    pandas.DataFrame: A copy of the input DataFrame with a new column 'number_of_balcony'
    containing extracted balcony numbers as floats.

    """
    df["number_of_balcony"] = df["number_of_balcony"].str.extract("(\\d+[\\.\\d]*)").astype(float)
    return df

# filter_by_range()
def filter_by_range(df, column, min_value, max_value):
    """Filters a DataFrame by a specified range of values in a given column.

    Args:
        df (pandas.DataFrame): The DataFrame to filter.
        column (str): The name of the column to filter.
        min_value (float or int): The minimum value to include in the filter range.
        max_value (float or int): The maximum value to include in the filter range.

    Returns:
        pandas.DataFrame: A filtered DataFrame containing only the rows where the specified
        column's values fall within the given range.

    """
    df = df[(df[column] >= min_value) & (df[column] <= max_value)]
    return df

# replace_flooring_material()
def replace_flooring_material(df):
    """Replace flooring material names in the 'flooring_material' column of the input
    DataFrame with their English equivalents using a dictionary of translations.

    Parameters:
    df (pandas.DataFrame): Input DataFrame with a column named 'flooring_material' that contains flooring material names.

    Returns:
    pandas.DataFrame: DataFrame with the 'flooring_material' column modified to contain English equivalents of the
    original flooring material names.

    """
    flooring_dict = {'Паркет': 'parquet', 'Ламинат': 'laminate',
                    'Мод': 'wood', 'Цемент': 'cement',
                    'Плита': 'tiles', 'Чулуу': 'stone'}
    df['flooring_material'] = df['flooring_material'].replace(flooring_dict)
    return df

# replace_garage()
def replace_garage(df):
    """Replace values in the 'garage' column of the given DataFrame with either 'yes' or
    'no' based on a predefined dictionary.

    Parameters:
    df (pandas.DataFrame): The input DataFrame.

    Returns:
    pandas.DataFrame: A copy of the input DataFrame with the 'garage' column values replaced.

    """
    garage_dict = {'Байгаа': 'yes', 'Байхгүй': 'no'}
    df['garage'] = df['garage'].replace(garage_dict)
    return df

# replace_window_type()
def replace_window_type(df):
    """Replaces the values in the 'window_type' column of a Pandas DataFrame with
    standardized values.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the 'window_type' column to be modified.

    Returns:
        pandas.DataFrame: The modified DataFrame with standardized 'window_type' values.

    """
    window_dict = {'Вакум': 'vinyl', 'Модон вакум': 'vinwood', 'Мод': 'wood', 'Төмөр вакум': 'viniron'}
    df['window_type'] = df['window_type'].replace(window_dict)
    return df

# replace_door_type()
def replace_door_type(df):
    """" Replaces Mongolian Cyrillic door types with their English equivalents.

    Args:
        df (pandas.DataFrame): The input pandas DataFrame.

    Returns:
        pandas.DataFrame: The input DataFrame with the 'door_type' column modified.

    Example:
        >>> df = pd.DataFrame({'door_type': ['Бүргэд', 'Төмөр вакум', 'Мод']})
        >>> replace_door_type(df)
            door_type
        0   burged
        1   ironvacuum
        2   wood

    """
    door_dict = {'Бүргэд': 'burged', 'Төмөр': 'iron',
                 'Төмөр вакум': 'ironvacuum', 'Вакум': 'vacuum',
                 'Мод': 'wood'}
    df['door_type'] = df['door_type'].replace(door_dict)
    return df

# replace_lease_type()
def replace_lease_type(df):
    """Replaces the Mongolian Cyrillic lease type value in the 'leasing' column of the
    given DataFrame with their English equivalents.

    Args:
    - df (Pandas DataFrame): The DataFrame that contains the 'leasing' column with lease type values.

    Returns:
    - The updated DataFrame with the lease type values replaced with readable strings.

    """
    lease_dict = {'Банкны лизингтэй': 'withlease', 'Лизинггүй': 'nolease', 'Хувь лизингтэй': 'privlease'}
    df['leasing'] = df['leasing'].replace(lease_dict)
    return df

def clean_manual(df):
    # fix errors manually
    # rents
    df = df[df['title'] != 'Nisekh, buman zaluus khoroolold 2 oroo bair']
    df = df[~((df['title'] == 'TSambagarawd 2oroo')&(df['price'] == 1))]

    # land
    df = df[~((df['title'] == 'Towiin shugamtai')&(df['price'] == 210))]


    # wrong m2
    mask = (df['title'] == 'Sky garden-d 3 oroo bair') & (df['price'] == 860)
    df.loc[mask, 'area_sq_m'] = 106
    mask = (df['title'] == 'Olimp hothond 67mk 3 uruu bair') & (df['price'] == 245)
    df.loc[mask, 'area_sq_m'] = 67

    # wrong price
    mask = (df['title'] == 'Bella vista-d 3 oroo') & (df['price'] == 10600)
    df.loc[mask, 'price'] = 1060
    mask = (df['title'] == 'YAarmagt 2 oroo bair') & (df['price'] == 1500)
    df.loc[mask, 'price'] = 150
    mask = (df['title'] == 'River garden modun taun 2 oroo') & (df['price'] == 25.8)
    df.loc[mask, 'price'] = 258
    mask = (df['title'] == 'Zaisand 4 oroo bair') & (df['price'] == 98)
    df.loc[mask, 'price'] = 980
    mask = (df['title'] == 'KHotыn towd 2 oroo bair') & (df['price'] == 40)
    df.loc[mask, 'price'] = 261.8


    # those seemingly missing 0 in the price, below 11 is m2 price, above 15 is total price
    df['price_orig'] = df['price']
    df['price_m2']   = df['price']
    mask = (df['price'].between(11, 15)) & (~df['title'].str.contains('220'))
    df.loc[mask, 'price'] = df.loc[mask, 'price'] * 10

    # price_m2
    mask = df['price'] > 11
    df.loc[mask, 'price_m2'] = df.loc[mask, 'price'] / df.loc[mask, 'area_sq_m']

    return df