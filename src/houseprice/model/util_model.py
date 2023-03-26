from patsy import dmatrices
from sklearn.model_selection import train_test_split
import re
import os
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

def create_model_data(formula,df,test_size=0.3,random_state=100):
    y, x = dmatrices(formula, df, return_type="dataframe")
    x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, random_state=random_state)

    return x_train, x_test, y_train, y_test

def remove_sym_name_df(df):
    regex = re.compile(r"\[|\]|<", re.IGNORECASE)
    df.columns = [regex.sub("_", col) if any(x in str(col) for x in set(('[', ']', '<'))) else col for col in df.columns.values]
    return df

def loop_cv(models, x_train, y_train, produces):
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

    return scores

def pick_save_model(models, scores=0, produces=None):
    my_model = models[np.argmax(scores)]
    pickle.dump(my_model, open(produces, "wb"))


def tune_model(model, param_grid, x_train, y_train):
    grid = GridSearchCV(model, param_grid, n_jobs=-1, cv=5)
    grid.fit(x_train, y_train)
    model = grid.best_estimator_

    return model

def calculate_diagnostics(y_test, y_pred):
    out = {}
    out['best_model'] = {
        "mse": mean_squared_error(y_test, y_pred),
        "r2" : r2_score(y_test, y_pred)}

    stats = pd.DataFrame(out)

    return stats

def fetch_data(folder_path):
    y_train = pd.read_pickle(os.path.join(folder_path, "y_train.pkl")).values.ravel()
    y_test  = pd.read_pickle(os.path.join(folder_path, "y_test.pkl")).values.ravel()
    x_train = pd.read_pickle(os.path.join(folder_path, "x_train.pkl"))
    x_test  = pd.read_pickle(os.path.join(folder_path, "x_test.pkl"))

    x_train = remove_sym_name_df(x_train)
    x_test  = remove_sym_name_df(x_test)

    return y_train, y_test, x_train, x_test
