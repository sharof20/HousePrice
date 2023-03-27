# Project Name: HousePrice

The HousePrice project involves building a machine learning model that accurately
estimates the prices of houses. This project can be useful for real estate
professionals, homeowners, and anyone else interested in predicting the value of
residential properties.

## How to Get Started:

To start working on the HousePrice project, follow these steps:

1. Clone the repository: This will create a local copy of the project on your machine.

1. Create a Conda environment: Use the following command to create an environment
   specifically for this project and activate it:

   ```
   $ conda/mamba env create
   ```

   ```
   $ conda activate houseprice
   ```

   This will help you manage dependencies and ensure that you have the necessary
   packages installed.

1. Install Pre-commit, Pytask, and Pytest: These are tools that help you maintain code
   quality, automate tasks, and test your code.

   ```
   $ pip install pre-commit
   ```

   ```
   $ pip install pytask
   ```

   ```
   $ pip install -U pytest
   ```

1. Install [Chromedriver](https://chromedriver.chromium.org/downloads): This is required
   to run the project, and you should ensure that you have a version that is compatible
   with your Chrome browser.

## Usage:

Once you have set up the environment and installed the necessary packages, you can build
the project using the following command:

```
$ pytask
```

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
We appreciate the contributions of the open-source community in creating and maintaining
these tools.
