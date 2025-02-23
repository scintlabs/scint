from __future__ import annotations
from typing import Optional

from scint.lib.switch import Request
from scint.lib.util.utils import env


class ScintInterface:
    SCINT_API_KEY: str = None
    SCINT_URL: str = "https://api.scint.co"

    def __init__(self, api_key: Optional[str] = None, url: Optional[str] = None):
        self.token = api_key or env("SCINT_API_KEY")
        self.server_url = url or self.DEFAULT_SERVER_URL

    async def messages(self, request: Request):
        pass

    async def tasks(self, request: Request):
        pass

    async def library(self, request: Request):
        pass

    async def settings(self, request: Request):
        pass

    async def find(self, request: Request):
        pass
