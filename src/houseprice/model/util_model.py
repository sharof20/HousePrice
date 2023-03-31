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
from houseprice.utilities import save_close_plt


def create_model_data(formula, df, test_size=0.3, random_state=100):
    """Splits a Pandas DataFrame into training and testing datasets, and returns the
    corresponding X and Y matrices for the training and testing datasets, based on the
    formula provided.

    Args:
        formula (str): A string representing the formula to use for creating the design matrices. The formula should
            be in the format of 'Y ~ X1 + X2 + ... + Xn', where Y is the dependent variable and X1 through Xn are the
            independent variables. The formula should be compatible with the Patsy library.
        df (pandas.DataFrame): A Pandas DataFrame containing the data to be split into training and testing datasets.
        test_size (float, optional): The proportion of the dataset to include in the test split. Defaults to 0.3.
        random_state (int, optional): Controls the shuffling applied to the data before applying the split. Pass an
            int for reproducible output across multiple function calls. Defaults to 100.

    Returns:
        tuple: A tuple of four elements, containing the training and testing datasets for the independent variables (X)
            and dependent variable (Y). The tuple is in the order of (x_train, x_test, y_train, y_test).

    """
    # Create the design matrices for the dependent and independent variables using the formula
    y, x = dmatrices(formula, df, return_type="dataframe")

    # Split the data into training and testing datasets for the dependent and independent variables
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

    # Return the training and testing datasets for the dependent and independent variables
    return x_train, x_test, y_train, y_test



def remove_sym_name_df(df):
    """Replaces square brackets and angle brackets in column names of a Pandas DataFrame
    with underscores.

    Args:
        df (pandas.DataFrame): A Pandas DataFrame whose column names are to be modified.

    Returns:
        pandas.DataFrame: A Pandas DataFrame with column names modified by replacing square brackets and angle brackets
            with underscores.

    """
    # Compile a regular expression pattern that matches square brackets and angle brackets
    regex = re.compile(r"\[|\]|<", re.IGNORECASE)

    # Modify the column names of the DataFrame by replacing square brackets and angle brackets with underscores,
    # but keep the original names if they don't contain any of these special characters
    df.columns = [regex.sub("_", col) if any(x in str(col) for x in set(('[', ']', '<'))) else col for col in df.columns.values]

    # Return the modified DataFrame
    return df



def loop_cv(models, x_train, y_train, produces):
    """Performs k-fold cross-validation on a list of machine learning models using the
    specified training data, and returns the median R-squared score for each model.

    Args:
        models (list): A list of tuples, each containing the name of a machine learning model and the model object.
        x_train (pandas.DataFrame): A Pandas DataFrame containing the training features.
        y_train (pandas.Series): A Pandas Series containing the target variable for the training set.
        produces (pathlib.Path): A pathlib.Path object specifying the output directory for the algorithm comparison plot
            and statistics file.

    Returns:
        list: A list of median R-squared scores, one for each model in the input list.

    """
    out = {}
    results = []
    names = []
    scores = []

    # Loop through each model in the input list
    for name, model in models:
        # Set up k-fold cross-validation
        kfold = KFold(n_splits=2, shuffle=True, random_state=123)

        # Perform k-fold cross-validation and store the results
        cv_results = cross_val_score(model, x_train, y_train, cv=kfold, scoring='r2')
        results.append(cv_results)
        names.append(name)

        # Store the mean, median, and standard deviation of the R-squared scores for this model
        out[name] = {
        "r2_mean": cv_results.mean(),
        "r2_median": np.median(cv_results),
        "r2_std" : cv_results.std()
        }

        # Append the median R-squared score for this model to the scores list
        scores.append(np.median(cv_results))

    # Compare Algorithms
    # Plot a box plot of the R-squared scores for each model
    plt.boxplot(results, labels=names)
    plt.title('Algorithm Comparison')
    plt.xticks(rotation=-90)
    plt.subplots_adjust(bottom=0.2)
    save_close_plt(produces / "compare_models.png")

    # Write the statistics for each model to a CSV file
    stats = pd.DataFrame(out)
    stats.to_csv(produces / "compare_models_stat.csv")

    # Return a list of median R-squared scores, one for each model in the input list
    return scores



def pick_save_model(models, scores=0, produces=None):
    """This function selects the best model from a list of models based on the highest
    score and saves it as a binary file using pickle.

    Parameters:
    -----------
    models : list
        List of models to be compared.
    scores : list or array-like, default=0
        List of scores corresponding to each model in the 'models' list. If 0, the function will not consider the scores.
    produces : str or Path, default=None
        File path to save the selected model.

    Returns:
    --------
    None
        The function saves the selected model as a binary file.

    """
    my_model = models[np.argmax(scores)]
    pickle.dump(my_model, open(produces, "wb"))



def tune_model(model, param_grid, x_train, y_train):
    """This function performs hyperparameter tuning on a model using GridSearchCV and
    returns the best estimator.

    Parameters:
    -----------
    model : estimator object
        This is the model for which we want to perform hyperparameter tuning.
    param_grid : dict
        This is a dictionary containing hyperparameters and their values to be tested.
    x_train : array-like
        This is the feature matrix to be used for training the model.
    y_train : array-like
        This is the target vector to be used for training the model.

    Returns:
    --------
    estimator object
        This is the best estimator that was found during the grid search.

    """
    grid = GridSearchCV(model, param_grid, n_jobs=-1, cv=5)
    grid.fit(x_train, y_train)
    model = grid.best_estimator_

    return model



def calculate_diagnostics(y_test, y_pred):
    """This function calculates the mean squared error and R^2 score for a model's
    predictions and returns them in a pandas DataFrame.

    Parameters:
    -----------
    y_test : array-like
        The true target values for the test set.
    y_pred : array-like
        The predicted target values for the test set.

    Returns:
    --------
    pandas DataFrame
        A DataFrame containing the calculated mean squared error and R^2 score for the predicted values.

    """
    out = {}
    out['best_model'] = {
        "mse": mean_squared_error(y_test, y_pred),
        "r2" : r2_score(y_test, y_pred)}

    stats = pd.DataFrame(out)

    return stats



def fetch_data(folder_path):
    """This function loads the data files from a folder and returns the data as arrays.

    Parameters:
    -----------
    folder_path : str
        The path to the folder containing the data files.

    Returns:
    --------
    tuple of arrays
        A tuple containing the following arrays: y_train, y_test, x_train, x_test.

    """
    y_train = pd.read_pickle(os.path.join(folder_path, "y_train.pkl")).values.ravel()
    y_test  = pd.read_pickle(os.path.join(folder_path, "y_test.pkl")).values.ravel()
    x_train = pd.read_pickle(os.path.join(folder_path, "x_train.pkl"))
    x_test  = pd.read_pickle(os.path.join(folder_path, "x_test.pkl"))

    x_train = remove_sym_name_df(x_train)
    x_test  = remove_sym_name_df(x_test)

    return y_train, y_test, x_train, x_test

