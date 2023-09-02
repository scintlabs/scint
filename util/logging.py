import sys

from loguru import logger


logfile = "[{time:YY-MM-DD HH:mm}] {name}.{function}: {message}"
cli = "<bold>{level}</bold> <fg #bbd4fb>{message}</fg #bbd4fb>"


logger.remove()
logger.add(
    "base/data/logs/logfile",
    rotation="10 MB",
    format=logfile,
    level="INFO",
    enqueue=True,
)
logger.add(sys.stderr, format=cli, level="INFO", enqueue=False)
