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
@pytask.mark.produces(BLD / "python" / "data" / "house_price_clean.csv")
def task_clean_data_python(depends_on, produces):
    """Clean the data (Python version)."""
    data = pd.read_csv(depends_on["data"])
    data = clean_data(data)
    data.to_csv(produces, index=False)
