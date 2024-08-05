from __future__ import annotations

import asyncio
from types import SimpleNamespace

import falcon
from falcon.asgi import App as Falcon

from scint.base.settings import Settings
from scint.base.utils import get_module


class Server(Falcon):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.set_services()

    def set_services(self):
        self.services = SimpleNamespace()
        for key, value in self.settings.services.as_dict().items():
            module_name = value.get("name")
            module_import_path = value.get("import_path")
            module_settings = value.get("settings")
            module = get_module(module_import_path, module_name)
            module = module(**module_settings)
            services = getattr(self, "services")
            setattr(services, module_name.lower(), module)
