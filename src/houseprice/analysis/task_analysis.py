# # 1. data_exploration
# # 2. model_selection
# # # try different models on the data, do cross validation and pick the best model

import pandas as pd
import pytask
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pdb
from houseprice.config import BLD, SRC
from houseprice.utilities import save_close_plt

# sns.set_theme()

@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "price_by_location.png")
def task_toy(depends_on, produces):
    df = pd.read_csv(depends_on)

    above5_ads = df.groupby('location')['location'].transform('count') > 5
    df = df.loc[above5_ads,]

    grouped = df.loc[:,['location', 'price_m2']] \
        .groupby(['location']) \
        .median() \
        .sort_values(by='price_m2')

    sns.boxplot(x=df.location, y=df.price_m2, order=grouped.index)
    plt.xticks(fontsize=10, rotation=90)
    plt.subplots_adjust(bottom=0.2)

    save_close_plt(produces)



@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "histogram_price.png")
def task_hist(depends_on, produces):
    df = pd.read_csv(depends_on)
    fig = px.histogram(df, x="price_m2")
    fig.write_image(produces)

@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "histogram_area.png")
def task_hist(depends_on, produces):
    df = pd.read_csv(depends_on)
    fig = px.histogram(df, x="area_sq_m")
    fig.write_image(produces)



@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "histogram_price_total.png")
def task_hist(depends_on, produces):
    df = pd.read_csv(depends_on)
    fig = px.histogram(df, x="price")
    fig.write_image(produces)



vars = ['number_of_balcony', \
        'year_of_commissioning','number_of_storeys','apartment_storey', \
        'number_of_windows','garage','flooring_material', \
        'window_type','door_type','construction_progress']

for var in vars:
    @pytask.mark.task
    @pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
    @pytask.mark.produces(BLD  / "plot" / f"price_{var}.png")
    def task_toy(depends_on, produces, myvar = var):
        df = pd.read_csv(depends_on)
        grouped = df.loc[:,[myvar, 'price_m2']] \
            .groupby([myvar]) \
            .median() \
            .sort_values(by='price_m2')

        sns.boxplot(x=df[myvar], y=df.price_m2, order=grouped.index)
        plt.xticks(fontsize=10, rotation=90)
        plt.subplots_adjust(bottom=0.2)

        save_close_plt(produces)


@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "price_area.png")
def task_price_area_dist(depends_on, produces):
    # read data from csv
    df = pd.read_csv(depends_on)
    # create scatter plot
    fig = px.scatter(df, x='area_sq_m', y='price_m2', color='district')

    fig.write_image(produces)

@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "price_year.png")
def task_price_year(depends_on, produces):
    # read data from csv
    df = pd.read_csv(depends_on)
    # create line chart
    grouped = df.groupby(['year_of_commissioning'])['price_m2'].mean().reset_index()
    fig = px.line(grouped, x='year_of_commissioning', y='price_m2')

    fig.write_image(produces)