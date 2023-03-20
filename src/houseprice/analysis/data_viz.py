import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt # visualization
import seaborn as sb # visualization

# read data from csv
df = pd.read_csv('house_price_clean.csv')

# divide column A by column B and create a new column C
df['price_per_sqm'] = df['area_sq_m'] / df['price_mln_MNT']

# group the data by flooring material and calculate the mean price per square meter
grouped = df.groupby(['flooring_material'])['price_per_sqm'].mean().reset_index()

# create a bar chart using Plotly Express
fig = px.bar(grouped, x='flooring_material', y='price_per_sqm')

# set the chart title and axis labels
fig.update_layout(
    title='Average Price per Square Meter by Flooring Material',
    xaxis_title='Flooring Material',
    yaxis_title='Price per Square Meter'
)

# display the chart
fig.show()

# create scatter plot
fig = px.scatter(df, x='area_sq_m', y='price_per_sqm', color='district')
fig.show()

# create line chart
grouped = df.groupby(['year_of_commissioning'])['price_per_sqm'].mean().reset_index()
fig = px.line(grouped, x='year_of_commissioning', y='price_per_sqm')
fig.show()

# create a histogram using seaborn
sb.histplot(x='area_sq_m', data=df, color='red')

# set the chart title and axis labels
plt.title('Distribution of Areas', fontsize=16)
plt.xlabel('Area (square meters)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

# set the font size of the tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# display the chart
plt.show()


# create a scatterplot using seaborn
sb.scatterplot(x='price_per_sqm', y='area_sq_m', data=df, color='yellow', edgecolor='blue', s=150)

# set the chart title and axis labels
plt.title('Price per Square Meter vs. Area', fontsize=16)
plt.xlabel('Price per Square Meter', fontsize=12)
plt.ylabel('Area (square meters)', fontsize=12)

# set the font size of the tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# display the chart
plt.show()

# create a scatterplot using seaborn
sb.scatterplot(x='area_sq_m', y='price_mln_MNT', data=df, color='orange', edgecolor='blue', s=150)

# set the chart title and axis labels
plt.title('Price vs. Area', fontsize=16)
plt.xlabel('Area (square meters)', fontsize=12)
plt.ylabel('Price (million MNT)', fontsize=12)

# set the font size of the tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# display the chart
plt.show()

# create a histogram using seaborn
sb.histplot(x='price_mln_MNT', data=df, color='green')

# set the chart title and axis labels
plt.title('Distribution of price_mln_MNT', fontsize=16)
plt.xlabel('price_mln_MNT)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)

# set the font size of the tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# display the chart
plt.show()
