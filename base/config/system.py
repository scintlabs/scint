import json
import os
from typing import Dict, Optional, Union

import dotenv
from pydantic import BaseModel
from xdg_base_dirs import xdg_cache_home, xdg_config_home, xdg_data_home

from base.config.logging import logger


def envar(var: str) -> Optional[str]:
    dotenv.load_dotenv()
    return os.environ.get(var)


name: str | os.PathLike = "scint"
scint_data = os.path.join(xdg_data_home(), name)
scint_config = os.path.join(xdg_config_home(), name)
scint_cache = os.path.join(xdg_cache_home(), name)

openai_key: str | None = envar("OPENAI_API_KEY")
discord_token: str | None = envar("DISCORD_TOKEN")


def _load(self) -> Union[Dict, None]:
    try:
        with open(scint_data, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        logger.warning(f"State file {scint_data} not found.")
        return None


def _save(self):
    data = {
        "status": self.status,
        "buffer": self.buffer,
        "capabilities": self.capabilities,
    }
    with open(scint_data, "w") as file:
        json.dump(data, file)
