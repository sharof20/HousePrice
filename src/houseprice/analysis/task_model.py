from houseprice.config import BLD

import pandas as pd
import numpy as np
import re
import os
import pickle
import pytask
import matplotlib.pyplot as plt
import xgboost as xgb
from patsy import dmatrices
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV


regex = re.compile(r"\[|\]|<", re.IGNORECASE)

@pytask.mark.depends_on(BLD / "data" / "house_price_clean_loc.csv")
@pytask.mark.produces(BLD  / "model" / "data")
def task_model_data(depends_on, produces):
    if not os.path.isdir(produces):
        os.makedirs(produces)
    df = pd.read_csv(depends_on)

    formula = "price_m2 ~ location + area_sq_m + number_of_balcony + \
               year_of_commissioning + number_of_storeys + apartment_storey + \
               number_of_windows + garage + flooring_material + \
               window_type + door_type + construction_progress"

    y, x = dmatrices(formula, df, return_type="dataframe")

    x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.3, random_state=100
        )

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
    y_train = pd.read_pickle(os.path.join(depends_on['data'], "y_train.pkl")).values.ravel()
    x_train = pd.read_pickle(os.path.join(depends_on['data'], "x_train.pkl"))
    x_test = pd.read_pickle(os.path.join(depends_on['data'], "x_test.pkl"))

    models = []
    # models.append(('SVM',svm.SVR()))
    # models.append(('Bayesian Ridge',linear_model.BayesianRidge()))
    # models.append(('Lasso Lars',linear_model.LassoLars()))
    # models.append(('ARD',linear_model.ARDRegression()))
    # models.append(('TheilSen',linear_model.TheilSenRegressor()))
    # models.append(('Linear',linear_model.LinearRegression()))
    # models.append(('GB',ensemble.GradientBoostingRegressor()))
    # models.append(('AdaBoost',ensemble.AdaBoostRegressor()))
    # models.append(('RandomForest',ensemble.RandomForestRegressor()))
    models.append(('DecisionTree',tree.DecisionTreeRegressor()))
    models.append(('XGB',xgb.XGBRegressor()))

    x_train.columns = [regex.sub("_", col) if any(x in str(col) for x in set(('[', ']', '<'))) else col for col in x_train.columns.values]
    x_test.columns = [regex.sub("_", col) if any(x in str(col) for x in set(('[', ']', '<'))) else col for col in x_test.columns.values]

    out = {}
    results = []
    names = []
    scores = []
    for name, model in models:
        kfold = KFold(n_splits=2, shuffle=True, random_state=123)
        cv_results = cross_val_score(model, x_train, y_train, cv=kfold, scoring='r2')
        results.append(cv_results)
        names.append(name)

        out[name] = {
        "r2_mean": cv_results.mean(),
        "r2_median": np.median(cv_results),
        "r2_std" : cv_results.std()
        }

        scores.append(np.median(cv_results))

    # Compare Algorithms
    plt.boxplot(results, labels=names)
    plt.title('Algorithm Comparison')
    plt.savefig(produces / "compare_models.png")

    stats = pd.DataFrame(out)
    stats.to_csv(produces / "compare_models_stat.csv")

    # pick the best model - without tuning
    # my_model = models[np.argmax(scores)]
    my_model = ('XGB',xgb.XGBRegressor()) # choose XGB as it frequently beats the rest. But it is bordering on RF and GB
    pickle.dump(my_model, open(produces / "model_notTuned.sav", "wb"))




@pytask.mark.depends_on(
        {"data": BLD / "model" / "data",
         "model": BLD / "model" / "model"}
        )
@pytask.mark.produces(BLD  / "model" / "prediction"  / "model_tuned.sav")
def task_model_tune(depends_on, produces):
    if not os.path.isdir(BLD  / "model" / "prediction"):
        os.makedirs(BLD  / "model" / "prediction")
    y_train = pd.read_pickle(os.path.join(depends_on['data'], "y_train.pkl")).values.ravel()
    x_train = pd.read_pickle(os.path.join(depends_on['data'], "x_train.pkl"))
    y_test = pd.read_pickle(os.path.join(depends_on['data'], "y_test.pkl")).values.ravel()
    x_test = pd.read_pickle(os.path.join(depends_on['data'], "x_test.pkl"))

    Y_train = y_train
    x_train = x_train
    x_train.columns = [regex.sub("_", col) if any(x in str(col) for x in set(('[', ']', '<'))) else col for col in x_train.columns.values]
    x_test.columns = [regex.sub("_", col) if any(x in str(col) for x in set(('[', ']', '<'))) else col for col in x_test.columns.values]


    model = pickle.load(open(os.path.join(depends_on['model'], "model_notTuned.sav"), "rb"))
    name = model[0]
    estimator = model[1]
    # param_grid = {'bootstrap': [True, False],
    #         'min_samples_split': [2, 4, 6],
    #         'n_estimators': [100,150,200]}

    param_grid={"max_depth": [ 5, 10, 15],           # 10
                "eta": [0.05, 0.10, 0.15, 0.20],     # learning_rate 0.15
                "min_child_weight": [ 1, 2, 3],      # 2
                "gamma":[ 0.1, 0.2, 0.3],            # min_split_loss 0.1
                "colsample_bytree":[ 0.25 , 0.5, 1], # 0.25, 0.3
                "n_estimators":[75, 100, 125]
                }

    param_grid={"max_depth": [ 5, 10]}

    grid = GridSearchCV(estimator, param_grid, n_jobs=-1, cv=5)

    grid.fit(x_train, y_train)
    model = grid.best_estimator_

    pickle.dump(model, open(produces, "wb"))



@pytask.mark.depends_on(
        {"data": BLD / "model" / "data",
         "model": BLD / "model" / "prediction"  / "model_tuned.sav"}
        )
@pytask.mark.produces(BLD  / "model" / "prediction"  / "prediction_stat.csv")
def task_model_pred(depends_on, produces):
    y_test = pd.read_pickle(os.path.join(depends_on['data'], "y_test.pkl")).values.ravel()
    x_test = pd.read_pickle(os.path.join(depends_on['data'], "x_test.pkl"))
    x_test.columns = [regex.sub("_", col) if any(x in str(col) for x in set(('[', ']', '<'))) else col for col in x_test.columns.values]

    model = pickle.load(open(os.path.join(depends_on['model']), "rb"))

    y_pred = model.predict(x_test)

    out = {}
    out['best_model'] = {
    "mse": mean_squared_error(y_test, y_pred),
    "r2" : r2_score(y_test, y_pred)}

    stats = pd.DataFrame(out)
    stats.to_csv(produces)