# # 1. data_exploration
# # 2. model_selection
# # # try different models on the data, do cross validation and pick the best model

import pandas as pd
import pytask
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from patsy import dmatrices
import pdb
from houseprice.config import BLD, SRC
from houseprice.analysis import test_models
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
import numpy as np
from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble
from sklearn import tree


import os

@pytask.mark.depends_on(BLD / "data" / "house_price_clean_loc.csv")
@pytask.mark.produces(BLD  / "model" / "data")
def task_model_data(depends_on, produces):
    df = pd.read_csv(depends_on)

    # # Importing data
    df = pd.read_csv("bld\data\house_price_clean.csv")

    # # # Extract relevent features
    # df = df[['price_m2','number_of_balcony','year_of_commissioning','number_of_storeys',
    #         'area_sq_m','apartment_storey','number_of_windows','location','garage','flooring_material',
    #         'window_type','door_type','construction_progress']]

    formula = "price_m2 ~ location + area_sq_m + number_of_balcony + \
               year_of_commissioning + number_of_storeys + apartment_storey + \
               number_of_windows + garage + flooring_material + \
               window_type + door_type + construction_progress"
    y, x = dmatrices(formula, df, return_type="dataframe")

    x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.3, random_state=100
        )

    scaler = StandardScaler().fit(x_train)
    x_train_scaled = pd.DataFrame(scaler.transform(x_train))
    x_test_scaled = pd.DataFrame(scaler.transform(x_test))

    if not os.path.isdir(produces):
        os.makedirs(produces)

    x_train.to_pickle(produces / "x_train.pkl")
    x_test.to_pickle(produces / "x_test.pkl")
    y_train.to_pickle(produces / "y_train.pkl")
    y_test.to_pickle(produces / "y_test.pkl")

    # model = LinearRegression().fit(x_train, y_train.values.ravel())


    # y_pred = model.predict(x_test)

    # new_df = y_test.copy()
    # new_df['y_pred'] = y_pred
    # new_df['diff'] = new_df['y_pred'] - new_df['price_m2']
    # new_df.sort_values(by='diff', inplace=True)
    # new_df.to_csv(produces / "linreg.csv")

    classifiers = [
        svm.SVR(),
        linear_model.SGDRegressor(),
        linear_model.BayesianRidge(),
        linear_model.LassoLars(),
        linear_model.ARDRegression(),
        linear_model.PassiveAggressiveRegressor(),
        linear_model.TheilSenRegressor(),
        linear_model.LinearRegression(),
        ensemble.GradientBoostingRegressor(),
        ensemble.AdaBoostRegressor(),
        ensemble.RandomForestRegressor(),
        tree.DecisionTreeRegressor()]

    out = {}
    for item in classifiers:
        print(item)
        clf = item
        clf.fit(x_train, y_train.values.ravel())
        y_pred = clf.predict(x_test)

        print(r2_score(y_test, y_pred))

        out[item] = {
        "mse": mean_squared_error(y_test, y_pred),
        "r2" : r2_score(y_test, y_pred)}

# add here grid search with cross validation.
#

    stats = pd.DataFrame(out)
    stats.to_csv(produces / "reg_results.csv")



    # print(mean_squared_error(y_test, y_pred))
    # print(mean_absolute_error(y_test, y_pred))
    # print(r2_score(y_test.values.ravel(), y_pred))
    # pred_y = model.predict_proba(x_test)[:, 1].flatten()
    # out = {
    #     "mse": mean_squared_error(y_test, probs),
    #     "f1": f1_score(y_test, pred),
    #     "accuracy": accuracy_score(y_test, pred),
    #     "recall": recall_score(y_test, pred),
    #     "precision": precision_score(y_test, pred),
    # }


    # pdb.set_trace()
