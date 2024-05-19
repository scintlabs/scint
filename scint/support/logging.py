import json
import sys

from loguru import logger as log


logfile_format = "[{time:YY-MM-DD HH:mm}] {name}.{function}: {message}"
cli_format = "<bold>{level}</bold> <fg #bbd4fb>{message}</fg #bbd4fb>"

log.remove()
log.add(sys.stderr, format=cli_format, level="INFO", enqueue=False)


def log_event(event_type, event_data):
    """
    """
    extra = {"event_type": event_type, "event_data": json.dumps(event_data)}
    log.bind(**extra).info(f"Event logged: {event_type} {event_data}")
