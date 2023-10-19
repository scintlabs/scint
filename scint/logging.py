import json
import os
import sys

from loguru import logger
from xdg_base_dirs import xdg_data_home

data_home: str | os.PathLike = xdg_data_home()

logfile_path = os.path.join(data_home, "logs", "logfile")
eventlog_path = os.path.join(data_home, "logs", "eventlog")

logfile_format = "[{time:YY-MM-DD HH:mm}] {name}.{function}: {message}"
cli_format = "<bold>{level}</bold> <fg #bbd4fb>{message}</fg #bbd4fb>"

logger.remove()

logger.add(
    logfile_path,
    rotation="10 MB",
    format=logfile_format,
    level="INFO",
    enqueue=True,
)
logger.add(
    eventlog_path,
    rotation="1 day",
    format=logfile_format,
    level="INFO",
    enqueue=True,
)
logger.add(sys.stderr, format=cli_format, level="INFO", enqueue=False)


def log_event(event_type, event_data):
    extra = {"event_type": event_type, "event_data": json.dumps(event_data)}
    logger.bind(**extra).info(f"Event logged: {event_type} {event_data}")
