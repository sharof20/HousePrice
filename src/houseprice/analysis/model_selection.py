from sklearn.linear_model import (
    BayesianRidge,  # Bayesian algorithm
    ElasticNet,  # ElasticNet algorithm
    Lasso,  # Lasso algorithm
    LinearRegression,  # OLS algorithm
    Ridge,  # Ridge algorithm
)
from sklearn.model_selection import train_test_split  # data split

# DATA SPLIT

X_var = df[
    [
        "LotArea",
        "MasVnrArea",
        "BsmtUnfSF",
        "TotalBsmtSF",
        "1stFlrSF",
        "2ndFlrSF",
        "GrLivArea",
        "GarageArea",
        "WoodDeckSF",
        "OpenPorchSF",
    ]
].values
y_var = df["SalePrice"].values

X_train, X_test, y_train, y_test = train_test_split(
    X_var,
    y_var,
    test_size=0.2,
    random_state=0,
)


# MODELLING

# 1. OLS

ols = LinearRegression()
ols.fit(X_train, y_train)
ols_yhat = ols.predict(X_test)

# 2. Ridge

ridge = Ridge(alpha=0.5)
ridge.fit(X_train, y_train)
ridge_yhat = ridge.predict(X_test)

# 3. Lasso

lasso = Lasso(alpha=0.01)
lasso.fit(X_train, y_train)
lasso_yhat = lasso.predict(X_test)

# 4. Bayesian

bayesian = BayesianRidge()
bayesian.fit(X_train, y_train)
bayesian_yhat = bayesian.predict(X_test)

# 5. ElasticNet

en = ElasticNet(alpha=0.01)
en.fit(X_train, y_train)
en_yhat = en.predict(X_test)

# EVALUATION

# 1. Explained Variance Score


# R-squared
