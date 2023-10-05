import json
import os
from typing import Dict, Optional, Union

import dotenv
from xdg_base_dirs import xdg_cache_home, xdg_config_home, xdg_data_home

from base.system.logging import logger


def envar(var: str) -> Optional[str]:
    dotenv.load_dotenv()
    return os.environ.get(var)


NAME: str | os.PathLike = "scint"
DATA_DIR = os.path.join(xdg_data_home(), NAME)
CONVERSTIONS = os.path.join(DATA_DIR, "conversations")
CONFIG_DIR = os.path.join(xdg_config_home(), NAME)
CACHE_DIR = os.path.join(xdg_cache_home(), NAME)


OPENAI_API_KEY: str | None = envar("OPENAI_API_KEY")
DISCORD_TOKEN: str | None = envar("DISCORD_TOKEN")


def load_config(dir) -> Union[Dict, None]:
    try:
        with open(dir, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logger.warning(f"State file {dir} not found.")
        return None
