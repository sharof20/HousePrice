import pytask
import pandas as pd

from houseprice.config import NO_LONG_RUNNING_TASKS
from houseprice.data_collection import run_collection
from houseprice.config import BLD, SRC


@pytask.mark.skipif(NO_LONG_RUNNING_TASKS, reason="Skip long-running tasks.")
@pytask.mark.produces(BLD / "data" / "house_price.csv")
def task_webscraping(produces):
    data = run_collection()
    df = pd.DataFrame(data)
    df.to_csv(produces, index=False, encoding="utf-8-sig")
