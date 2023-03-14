from config import NO_LONG_RUNNING_TASKS


@pytask.mark.skipif(NO_LONG_RUNNING_TASKS, reason="Skip long-running tasks.")
@pytask.mark.depends_on("time_intensive_product.pkl")
def task_that_takes_really_long_to_run(depends_on):
