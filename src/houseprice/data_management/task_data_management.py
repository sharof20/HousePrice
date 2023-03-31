"""Tasks for data cleaning and featurization."""

import pandas as pd
import pytask

from houseprice.config import BLD, SRC
from houseprice.data_management import clean_data


@pytask.mark.depends_on(
    {
        "data": SRC / "data" / "house_price.csv", # NO_LONG_RUNNING_TASKS: change SRC to BLD if running webscraping
    },
)
@pytask.mark.produces(BLD / "data" / "house_price_clean_without_location.csv")
def task_clean_data_python(depends_on, produces):
    """Copy raw data."""
    data = pd.read_csv(depends_on["data"])
    data = clean_data(data)
    data.to_csv(produces, index=False, encoding="utf-8-sig")


# NOTE: For about 1/4 of the all ads, the location is missing.
# We can figure it out from the ad text, however. But
# cleaning location by this way is really messy and time consuming.
# Ideally, we would have a dictionary and functions which can map
# out the location from the text.
# We already put manually cleared locations in location_map.csv.
# In task_create_location, we copy it to BLD, just reflecting how we will create
# these locations by functions.
# By using ad's ID, we can map ad with its hand created location. That's
# how we do it below in task_clean_location. In the future, ideally, this task will be automated.

@pytask.mark.depends_on(
    {
        "data": BLD / "data" / "house_price_clean_without_location.csv",
        "location": SRC / "data" / "location_map.csv"
    },
)
@pytask.mark.produces(BLD / "data" / "location_map.csv")
def task_create_location(depends_on, produces):
    """Clean the location - raw sketch"""
    lctn = pd.read_csv(depends_on["location"])
    data = pd.read_csv(depends_on["data"])

    ### would handle location cleaning somewhere here
    # pass

    lctn.to_csv(produces, index=False, encoding="utf-8-sig")


@pytask.mark.depends_on(
    {
        "data": BLD / "data" / "house_price_clean_without_location.csv",
        "location": BLD / "data" / "location_map.csv",
    },
)
@pytask.mark.produces(BLD / "data" / "house_price_clean.csv")
def task_clean_location(depends_on, produces):
    """Data with clean location."""
    data = pd.read_csv(depends_on["data"])
    lctn = pd.read_csv(depends_on["location"])
    lctn = lctn[["ID","location_group"]]
    data = data.merge(lctn, on='ID', how='left')
    data = data.rename(columns={'location': 'location_data', 'location_group': 'location'})
    data.to_csv(produces, index=False, encoding="utf-8-sig")
