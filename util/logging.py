from loguru import logger
from util.env import envar

envar("XDG_DATA_HOME")

log_format = "[<fg #626261>{time:YY-MM-DD HH:mm}</fg #626261>] <blue>{name}</blue>: <cyan>{function}</cyan> | <level>{message}</level>"

logger.add("util/logfile", rotation="10 MB", format=log_format, level="INFO")
