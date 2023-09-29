import json
import sys

from loguru import logger

logfile = "[{time:YY-MM-DD HH:mm}] {name}.{function}: {message}"
cli = "<bold>{level}</bold> <fg #bbd4fb>{message}</fg #bbd4fb>"


logger.remove()

logger.add(
    "data/logs/logfile",
    rotation="10 MB",
    format=logfile,
    level="INFO",
    enqueue=True,
)
logger.add(
    "data/logs/eventlog", rotation="1 day", format=logfile, level="INFO", enqueue=True
)
logger.add(sys.stderr, format=cli, level="INFO", enqueue=False)


log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> | <cyan>{extra}</cyan>"


def log_event(event_type, event_data):
    extra = {"event_type": event_type, "event_data": json.dumps(event_data)}
    logger.bind(**extra).info("Event logged")


log_event("user_login", {"user_id": 123})
log_event("api_call", {"endpoint": "/data", "response_code": 200})
