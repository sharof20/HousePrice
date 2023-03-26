import pytask
import pandas as pd

from houseprice.config import NO_LONG_RUNNING_TASKS
from houseprice.data_collection import run_collection
from houseprice.config import BLD, SRC

# Pytask will skip the webscraping part due to lengthy time it takes.
# Change NO_LONG_RUNNING_TASKS to False in config.py if you
# want to run this part. In a laptop and without parallelization, it will take 8-10 hours.

@pytask.mark.skipif(NO_LONG_RUNNING_TASKS, reason="Skip long-running tasks.")
@pytask.mark.produces(BLD / "data" / "house_price.csv")
def task_webscraping(produces):
    data = run_collection()
    df = pd.DataFrame(data)
    df.to_csv(produces, index=False, encoding="utf-8-sig")
