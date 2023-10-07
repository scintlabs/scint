import json
import os
from typing import Dict, Optional, Union

import dotenv
from xdg_base_dirs import xdg_cache_home, xdg_config_home, xdg_data_home

from app.services.logging import logger


def envar(var: str) -> Optional[str]:
    dotenv.load_dotenv()
    return os.environ.get(var)


# appname
APPNAME: str | os.PathLike = "scint"

# keys/tokens
OPENAI_API_KEY: str | None = envar("OPENAI_API_KEY")
DISCORD_TOKEN: str | None = envar("DISCORD_TOKEN")

# data
APPDATA = os.path.join(xdg_data_home(), APPNAME)
CONVERSTIONS = os.path.join(APPDATA, "conversations")
LOGS = os.path.join(APPDATA, "logs")


def load_config(dir) -> Union[Dict, None]:
    try:
        with open(dir, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logger.warning(f"State file {dir} not found.")
        return None
