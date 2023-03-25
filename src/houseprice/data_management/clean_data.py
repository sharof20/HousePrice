"""Function(s) for cleaning the data set(s)."""
import pdb
from transliterate import translit
import re
import numpy as np

# Define a function to transliterate Mongolian Cyrillic to English
def transliterate_mn(text):
    return translit(text, 'mn', reversed=True)

def extract_price(x):
    price = float(re.findall('(\\d+[\\.\\d]*)', x)[0])
    if 'бум' in x and 'сая' not in x:
        return price * 1e3
    else:
        return price

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

    # df.reset_index(inplace=True)
    # pdb.set_trace()
    # df.price_m2.describe()
    # df.price_m2.unique()
    # df[df.price_m2<1]
    # df[df.price_m2>14]






    return df
