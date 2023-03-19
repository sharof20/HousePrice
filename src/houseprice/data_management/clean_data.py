"""Function(s) for cleaning the data set(s)."""
import pdb

import numpy as np


def clean_data(df):
    # drop the 'location:' and 'Koд:' columns as they are almost empty columns
    df = df.drop(["location:", "Код:"], axis=1)

    # create a dictionary of old and new column names
    new_names = {"Title": "title",
                "Price": "price_mln_MNT",
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
    df["price_mln_MNT"] = df["price_mln_MNT"].str.extract("(\\d+[\\.\\d]*)").astype(float)

    # extract numbers from the area_sq_m column and convert to float
    df["area_sq_m"] = df["area_sq_m"].str.extract("(\\d+[\\.\\d]*)").astype(float)

    # convert 'number_of_balcony:' column to string type before using .str accessor
    df["number_of_balcony"] = df["number_of_balcony"].astype(str)

    # replace 'Tarтryй', which means 'No balcony', with 0
    df["number_of_balcony"] = np.where(df["number_of_balcony"].str.contains("Tarтryй"), "0 Tarтryй", df["number_of_balcony"])

    # extract numbers from the Tarт column and convert to float
    df["number_of_balcony"] = df["number_of_balcony"].str.extract("(\\d+[\\.\\d]*)").astype(float)


    #the number of values dropped is 21

    #checking outliers in 'area_sq_m' column

    # filter out values below 10 and above 1000. The number of values dropped is 21
    df = df[(df["area_sq_m"] >= 10) & (df["area_sq_m"] <= 1000)]

    pdb.set_trace()

    return df
