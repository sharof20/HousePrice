from houseprice.config import BLD

import pandas as pd
import numpy as np
import os
import pickle
import pytask
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble
from sklearn import tree
from houseprice.model import util_model as ut


@pytask.mark.depends_on(BLD / "data" / "house_price_clean.csv")
@pytask.mark.produces(BLD  / "model" / "data")
def task_model_data(depends_on, produces):
    if not os.path.isdir(produces):
        os.makedirs(produces)
    df = pd.read_csv(depends_on)
    formula = "price_m2 ~ location + area_sq_m + number_of_balcony + \
               year_of_commissioning + number_of_storeys + apartment_storey + \
               number_of_windows + garage + flooring_material + \
               window_type + door_type + construction_progress"

    x_train, x_test, y_train, y_test = ut.create_model_data(formula, df)

    x_train.to_pickle(produces / "x_train.pkl")
    x_test.to_pickle(produces  / "x_test.pkl")
    y_train.to_pickle(produces / "y_train.pkl")
    y_test.to_pickle(produces  / "y_test.pkl")



@pytask.mark.depends_on(
        {"data": BLD / "model" / "data"}
        )
@pytask.mark.produces(BLD  / "model" / "model")
def task_model_select(depends_on, produces):
    if not os.path.isdir(produces):
        os.makedirs(produces)

    y_train, _, x_train, x_test = ut.fetch_data(depends_on['data'])

    models = []
    models.append(('SVM',svm.SVR()))
    models.append(('Bayesian Ridge',linear_model.BayesianRidge()))
    models.append(('Lasso Lars',linear_model.LassoLars()))
    models.append(('ARD',linear_model.ARDRegression()))
    models.append(('TheilSen',linear_model.TheilSenRegressor()))
    models.append(('Linear',linear_model.LinearRegression()))
    models.append(('GB',ensemble.GradientBoostingRegressor()))
    models.append(('AdaBoost',ensemble.AdaBoostRegressor()))
    models.append(('RandomForest',ensemble.RandomForestRegressor()))
    models.append(('DecisionTree',tree.DecisionTreeRegressor()))
    models.append(('XGB',xgb.XGBRegressor()))

    scores = ut.loop_cv(models, x_train, y_train, produces)

    # pick the best model - without tuning
    # ut.pick_save_model(models, scores, produces)
    # choose XGB as it frequently beats the rest. But it is bordering on RF and GB
    ut.pick_save_model([('XGB',xgb.XGBRegressor())], produces = produces  / "model_notTuned.sav")



@pytask.mark.depends_on(
        {"data": BLD / "model" / "data",
         "model": BLD / "model" / "model"}
        )
@pytask.mark.produces(BLD  / "model" / "prediction"  / "model_tuned.sav")
def task_model_tune(depends_on, produces):
    if not os.path.isdir(BLD  / "model" / "prediction"):
        os.makedirs(BLD  / "model" / "prediction")

    y_train, _, x_train, _ = ut.fetch_data(depends_on['data'])

    model = pickle.load(open(os.path.join(depends_on['model'], "model_notTuned.sav"), "rb"))
    name = model[0]
    estimator = model[1]

    param_grid={"max_depth": [ 5, 10, 15],           # 10
                "eta": [0.05, 0.10, 0.15, 0.20],     # learning_rate 0.15
                "min_child_weight": [ 1, 2, 3],      # 2
                "gamma":[ 0.1, 0.2, 0.3],            # min_split_loss 0.1
                "colsample_bytree":[ 0.25 , 0.5, 1], # 0.25, 0.3
                "n_estimators":[75, 100, 125]
                }

    param_grid={"max_depth": [ 5, 10]}

    model = ut.tune_model(estimator,param_grid,x_train, y_train)
    pickle.dump(model, open(produces, "wb"))



@pytask.mark.depends_on(
        {"data": BLD / "model" / "data",
         "model": BLD / "model" / "prediction"  / "model_tuned.sav"}
        )
@pytask.mark.produces(BLD  / "model" / "prediction"  / "prediction_stat.csv")
def task_model_pred(depends_on, produces):
    _, y_test, _, x_test = ut.fetch_data(depends_on['data'])

    model = pickle.load(open(os.path.join(depends_on['model']), "rb"))
    y_pred = model.predict(x_test)

    stats = ut.calculate_diagnostics( y_test, y_pred)
    stats.to_csv(produces)