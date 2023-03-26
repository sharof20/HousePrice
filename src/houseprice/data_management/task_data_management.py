"""Tasks for data cleaning and featurization."""

import pandas as pd
import pytask

from houseprice.config import BLD, SRC
from houseprice.data_management import clean_data


@pytask.mark.depends_on(
    {
        "data": SRC / "data" / "house_price.csv",
    },
)
@pytask.mark.produces(BLD / "data" / "house_price_clean.csv")
def task_clean_data_python(depends_on, produces):
    """Clean the data (Python version)."""
    data = pd.read_csv(depends_on["data"])
    data = clean_data(data)
    data.to_csv(produces, index=False, encoding="utf-8-sig")


@pytask.mark.depends_on(
    {
        "data": BLD / "data" / "house_price_clean.csv",
        "location": SRC / "data" / "location_map.csv",
    },
)
@pytask.mark.produces(BLD / "data" / "house_price_clean_loc.csv")
def task_clean_location(depends_on, produces):
    """Clean the data (Python version)."""
    data = pd.read_csv(depends_on["data"])
    lctn = pd.read_csv(depends_on["location"])
    lctn = lctn[["ID","location_group"]]
    data = data.merge(lctn, on='ID', how='left')
    data = data.rename(columns={'location': 'location_data', 'location_group': 'location'})
    data.to_csv(produces, index=False, encoding="utf-8-sig")
