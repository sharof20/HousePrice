import pytask

from houseprice.config import NO_LONG_RUNNING_TASKS
from houseprice.data_collection import run_collection


@pytask.mark.skipif(NO_LONG_RUNNING_TASKS, reason="Skip long-running tasks.")
@pytask.mark.depends_on("time_intensive_product.pkl")
def task_that_takes_really_long_to_run():
    run_collection()
