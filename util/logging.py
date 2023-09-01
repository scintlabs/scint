from loguru import logger
from util.env import envar

envar("XDG_DATA_HOME")

# cli_format = "[<fg #626261>{time:YY-MM-DD HH:mm}</fg #626261>] <blue>{name}</blue>.<cyan>{function}</cyan> | <level>{message}</level>"

log_format = "[{time:YY-MM-DD HH:mm}] {name}.{function}: {message}"

logger.add("logs/logfile", rotation="10 MB", format=log_format, level="INFO")
