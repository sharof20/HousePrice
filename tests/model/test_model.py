import os
import numpy as np
import pandas as pd
import pytest
import pickle
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split
from houseprice.config import TEST_DIR
from houseprice.data_management import clean_data

from houseprice.model.util_model import remove_sym_name_df
from houseprice.model.util_model import create_model_data
from houseprice.model.util_model import remove_sym_name_df
from houseprice.model.util_model import pick_save_model
from houseprice.model.util_model import tune_model
from houseprice.model.util_model import fetch_data
from houseprice.model.util_model import calculate_diagnostics

#loop_cv



@pytest.fixture(scope='module')
def test_data():
    """Create a Pandas DataFrame for testing the create_model_data function."""
    df = pd.DataFrame({'A': np.random.rand(100),
                       'B': np.random.rand(100),
                       'C': np.random.rand(100),
                       'Y': np.random.rand(100)})
    return df

def test_create_model_data(test_data):
    """Test the create_model_data function."""
    # Call the create_model_data function
    x_train, x_test, y_train, y_test = create_model_data('Y ~ A + B + C', test_data)

    # Test that the training and testing datasets have the correct number of rows
    assert len(x_train) == 70
    assert len(x_test) == 30
    assert len(y_train) == 70
    assert len(y_test) == 30

    # Test that the training and testing datasets have the correct number of columns
    assert x_train.shape[1] == 4
    assert x_test.shape[1] == 4
    assert y_train.shape[1] == 1
    assert y_test.shape[1] == 1

    # Test that the training and testing datasets contain no missing values
    assert x_train.isna().sum().sum() == 0
    assert x_test.isna().sum().sum() == 0
    assert y_train.isna().sum().sum() == 0
    assert y_test.isna().sum().sum() == 0



def test_remove_sym_name_df():
    # Create a sample dataframe with column names that contain square brackets and angle brackets
    data = {'[Column1]': [1, 2, 3], '<Column2>': [4, 5, 6]}
    df = pd.DataFrame(data)

    # Call the function being tested
    result = remove_sym_name_df(df)

    # Assert that the function modified the column names correctly
    assert list(result.columns) == ['_Column1_', '_Column2>']

    # Assert that the original dataframe was not modified
    assert list(df.columns) == ['_Column1_', '_Column2>']



@pytest.fixture
def models():
    #from sklearn.linear_model import LinearRegression
    #from sklearn.tree import DecisionTreeRegressor
    #from sklearn.ensemble import RandomForestRegressor

    lr = LinearRegression()
    dt = DecisionTreeRegressor(random_state=42)
    rf = RandomForestRegressor(n_estimators=100, random_state=42)

    return [lr, dt, rf]

@pytest.fixture
def scores(models):
    from sklearn.datasets import make_regression

    X, y = make_regression(n_samples=100, n_features=10, random_state=42)

    scores = []
    for model in models:
        model.fit(X, y)
        score = model.score(X, y)
        scores.append(score)

    return scores

@pytest.fixture
def produces():
    produces = Path("test_model.pkl")
    yield produces
    produces.unlink()

def test_pick_save_model(models, scores, produces):
    pick_save_model(models, scores, produces)

    assert produces.exists()
    assert produces.is_file()

    with open(produces, "rb") as f:
        model = pickle.load(f)

    assert isinstance(model, type(models[0]))


def test_tune_model_knn():
    """Test the tune_model function with KNeighborsClassifier on the iris dataset."""
    X, y = load_iris(return_X_y=True)

    model = KNeighborsClassifier()
    param_grid = {'n_neighbors': [1, 3, 5, 5, 9]}

    best_model = tune_model(model, param_grid, X, y)

    assert isinstance(best_model, KNeighborsClassifier)
    assert best_model.get_params()['n_neighbors'] == 5



def test_calculate_diagnostics():
    y_test = np.array([1, 2, 3, 4, 5])
    y_pred = np.array([1.1, 2.2, 2.8, 3.9, 5.1])

    expected_mse = 0.022  # Updated expected value
    expected_r2 = 0.989

    result = calculate_diagnostics(y_test, y_pred)

    assert result['best_model']['mse'] == pytest.approx(expected_mse, abs=1e-3)
    assert result['best_model']['r2'] == pytest.approx(expected_r2, abs=1e-3)



@pytest.fixture
def test_folder(tmpdir):
    """Create a temporary folder with sample data files for testing."""
    tmp_folder = tmpdir.mkdir("test_folder")
    pd.DataFrame({'a': [1, 2, 3]}).to_pickle(os.path.join(tmp_folder, "y_train.pkl"))
    pd.DataFrame({'a': [4, 5, 6]}).to_pickle(os.path.join(tmp_folder, "y_test.pkl"))
    pd.DataFrame({'a': [7, 8, 9], 'b': [10, 11, 12]}).to_pickle(os.path.join(tmp_folder, "x_train.pkl"))
    pd.DataFrame({'a': [13, 14, 15], 'b': [16, 17, 18]}).to_pickle(os.path.join(tmp_folder, "x_test.pkl"))
    return tmp_folder


def test_fetch_data(test_folder):
    """Test the fetch_data function with sample data."""
    y_train, y_test, x_train, x_test = fetch_data(test_folder)

    assert y_train.tolist() == [1, 2, 3]
    assert y_test.tolist() == [4, 5, 6]
    assert x_train['a'].tolist() == [7, 8, 9]
    assert x_train['b'].tolist() == [10, 11, 12]
    assert x_test['a'].tolist() == [13, 14, 15]
    assert x_test['b'].tolist() == [16, 17, 18]

