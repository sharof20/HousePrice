"""Function(s) for cleaning the data set(s)."""
import pdb
from transliterate import translit
import re
import numpy as np

# Define a function to transliterate Mongolian Cyrillic to English
def transliterate_mn(text):
    return translit(text, 'mn', reversed=True)

def extract_price(x):
    if 'бум' in x and 'сая' not in x:
        return float(re.findall('(\\d+[\\.\\d]*)', x)[0]) * 1000
    else:
        return float(re.findall('(\\d+[\\.\\d]*)', x)[0])

def clean_data(df):
    # drop the 'location:' and 'Koд:' columns as they are almost empty columns
    df = df.drop(["location:", "Код:"], axis=1)

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

    # display the updated DataFrame

    # extract numbers from the price column and convert to float
    df["price"] = df["price_text"].apply(extract_price)

    # extract numbers from the area_sq_m column and convert to float
    df["area_sq_m"] = df["area_sq_m"].str.extract("(\\d+[\\.\\d]*)").astype(float)

    # convert 'number_of_balcony:' column to string type before using .str accessor
    df["number_of_balcony"] = df["number_of_balcony"].astype(str)

    # replace 'Tarтryй', which means 'No balcony', with 0
    df["number_of_balcony"] = np.where(df["number_of_balcony"].str.contains("Tarтrүй"), "0 Tarтrүй", df["number_of_balcony"])

    # extract numbers from the Tarт column and convert to float
    df["number_of_balcony"] = df["number_of_balcony"].str.extract("(\\d+[\\.\\d]*)").astype(float)


    #the number of values dropped is 21

    #checking outliers in 'area_sq_m' column

    # filter out values below 10 and above 1000. The number of values dropped is 21
    df = df[(df["area_sq_m"] >= 10) & (df["area_sq_m"] <= 1000)]

    # Apply the function to the 'text' column
    df['location'] = df['location'].apply(transliterate_mn)
    df['district'] = df['district'].apply(transliterate_mn)
    df['title'] = df['title'].apply(transliterate_mn)

    flooring_dict = {'Паркет': 'parquet', 'Ламинат': 'laminate',
                        'Мод': 'wood', 'Цемент': 'cement',
                        'Плита': 'tiles', 'Чулуу': 'stone'}

    garage_dict = {'Байгаа': 'yes', 'Байхгүй': 'no'}
    window_dict = {'Вакум': 'vinyl', 'Модон вакум': 'vinwood',
                   'Мод': 'wood', 'Төмөр вакум': 'viniron'}
    door_dict   = {'Бүргэд': 'burged', 'Төмөр': 'iron',
                   'Төмөр вакум': 'ironvacuum', 'Вакум': 'vacuum',
                   'Мод': 'wood'}
    lease_dict  = {'Банкны лизингтэй': 'withlease', 'Лизинггүй': 'nolease',
                   'Хувь лизингтэй': 'privlease'}
    prog_dict   = {'Ашиглалтад орсон': 'complete', 'Ашиглалтад ороогүй': 'incomplete'}

    df['flooring_material'] = df['flooring_material'].replace(flooring_dict)
    df['garage'] = df['garage'].replace(garage_dict)
    df['window_type'] = df['window_type'].replace(window_dict)
    df['door_type'] = df['door_type'].replace(door_dict)
    df['leasing'] = df['leasing'].replace(lease_dict)
    df['construction_progress'] = df['construction_progress'].replace(prog_dict)

    # those seemingly missing 0 in the price, below 11 is m2 price, above 15 is total price
    df['price_orig'] = df['price']
    df['price_m2']   = df['price']
    mask = (df['price'].between(11, 15)) & (~df['title'].str.contains('220'))
    df.loc[mask, 'price'] = df.loc[mask, 'price'] * 10

    # price_m2
    mask = df['price'] > 11
    df.loc[mask, 'price_m2'] = df.loc[mask, 'price'] / df.loc[mask, 'area_sq_m']

    # pdb.set_trace()

    return df
