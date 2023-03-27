# House Price Project

The House Price project comprises of tasks for collecting apartment ads in Ulaanbaatar,
Mongolia placed in www.unegui.mn, the most popular portal site for ads and building a
machine learning model for estimating apartment prices.

The project utilizes and operates on the workflow management system
[pytask](https://pytask-dev.readthedocs.io/en/stable/index.html).

## How to Get Started:

To get started, follow these steps:

1. Clone the repository to have a local copy of the project on your machine.

1. Create a Conda environment specific to this project and activate it using the
   following commands:

   ```bash
   $ conda env create -f environment.yml
   $ conda activate houseprice
   ```

   This will help you manage dependencies and ensure that you have the necessary
   packages installed which are written down in the file environment.yml.

1. Install Chromedriver: This is not required to run the project by default and you can
   already proceed to the next step. We skip the task of data collection through
   webscraping in Chrome as it takes time (about 10 hours) and the rest of the tasks
   will use the data that we have already collected. Therefore, you can install
   chromedriver only if you want to collect data from scratch. Go
   [here](https://chromedriver.chromium.org/getting-started) to download and install the
   chromedriver on your machine. Make sure you have a version that is compatible with
   your Chrome browser.

On the other hand, if you want to run the webscraping part, then set
NO_LONG_RUNNING_TASKS to False in config.py under src folder.

## Usage:

### Running the project

Once you have set up the environment and installed the necessary packages, you can build
the project running the pytask command in the home folder of the project:

```bash
$ pytask
```

The project results will be created in bld folder. The project contains the following
tasks:

- data_collection/task_webscraping - it will be skipped by default. Read Chromedriver
  part above to run it.
- data_management/task_clean_data_python - clean raw data
- data_management/task_create_location - parsing locations
- data_management/task_clean_location - assigning cleaned location to ads
- 16 tasks creating visualization figures.
- model/task_model_data - preparing data matrices for modelling part
- model/task_model_select - picking the best model on the data out of multiple ML models
- model/task_model_tune - further fine tuning the chosen model
- model/task_model_pred - checking the prediction ability of the chosen model

## Tests

```bash
$ pytest
```

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).
We appreciate the contributions of the open-source community in creating and maintaining
these tools.
