# # 1. data_exploration
# # 2. model_selection
# # # try different models on the data, do cross validation and pick the best model

import pandas as pd
import pytask
import plotly.express as px
import plotly.graph_objects as go
from houseprice.config import BLD, SRC


@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "plot" / "histogram.png")
def task_hist(depends_on, produces):
    df = pd.read_csv(depends_on)
    fig = px.histogram(df, x="price_m2")
    fig.write_image(produces)

