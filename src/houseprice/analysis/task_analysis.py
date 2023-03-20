# # 1. data_exploration
# # 2. model_selection
# # # try different models on the data, do cross validation and pick the best model

import pandas as pd
import pytask
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sb
from houseprice.config import BLD, SRC


@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "histogram.png")
def task_hist(depends_on, produces):
    df = pd.read_csv(depends_on)
    fig = px.histogram(df, x="price_m2")
    fig.write_image(produces)

@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "price_flrMat.png")
def task_price_flrMat(depends_on, produces):
    # read data from csv
    df = pd.read_csv(depends_on)

    # group the data by flooring material and calculate the mean price per square meter
    grouped = df.groupby(['flooring_material'])['price_m2'].mean().reset_index()

    # create a bar chart using Plotly Express
    fig = px.bar(grouped, x='flooring_material', y='price_m2')

    # set the chart title and axis labels
    fig.update_layout(
        title='Average Price per Square Meter by Flooring Material',
        xaxis_title='Flooring Material',
        yaxis_title='Price per Square Meter'
    )

    fig.write_image(produces)

@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "price_area_dist.png")
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


@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "area_dist.png")
def task_area_dist(depends_on, produces):
    # read data from csv
    df = pd.read_csv(depends_on)
    # create a histogram using seaborn
    sb.histplot(x='area_sq_m', data=df, color='red')

    # set the chart title and axis labels
    plt.title('Distribution of Areas', fontsize=16)
    plt.xlabel('Area (square meters)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)

    # set the font size of the tick labels
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.savefig(produces)

@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "price_area.png")
def task_price_area(depends_on, produces):
    # read data from csv
    df = pd.read_csv(depends_on)

    # create a scatterplot using seaborn
    sb.scatterplot(x='price_m2', y='area_sq_m', data=df, color='yellow', edgecolor='blue', s=150)

    # set the chart title and axis labels
    plt.title('Price per Square Meter vs. Area', fontsize=16)
    plt.xlabel('Price per Square Meter', fontsize=12)
    plt.ylabel('Area (square meters)', fontsize=12)

    # set the font size of the tick labels
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.savefig(produces)

@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "total_price_area.png")
def task_total_price_area(depends_on, produces):
    # read data from csv
    df = pd.read_csv(depends_on)

    # create a scatterplot using seaborn
    sb.scatterplot(x='area_sq_m', y='price', data=df, color='orange', edgecolor='blue', s=150)

    # set the chart title and axis labels
    plt.title('Price vs. Area', fontsize=16)
    plt.xlabel('Area (square meters)', fontsize=12)
    plt.ylabel('Price (million MNT)', fontsize=12)

    # set the font size of the tick labels
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.savefig(produces)


@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "total_price_dist.png")
def task_total_price_dist(depends_on, produces):
    # read data from csv
    df = pd.read_csv(depends_on)

    # create a histogram using seaborn
    sb.histplot(x='price', data=df, color='green')

    # set the chart title and axis labels
    plt.title('Distribution of price', fontsize=16)
    plt.xlabel('price)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)

    # set the font size of the tick labels
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.savefig(produces)