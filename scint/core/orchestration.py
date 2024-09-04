from __future__ import annotations

import asyncio

from falcon.asgi import App

from scint.core import Core
from scint.core.architect import Architect
from scint.core.composer import Composer
from scint.core.components.handler import Handler
from scint.core.utils.helpers import get_module
from scint.resources.root import RootResource


class Orchestration(App, Core):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        with self.context() as ctx:
            app = ctx.create("app")
            self.init_services(app)
            self.init_core(app)
            self.add_handlers(app)
            self.add_routes()
            self.start_tasks()
            self.app = app

    def init_services(self, app):
        services = app.create("services")
        for key, value in self.settings.services.as_dict().items():
            self._set_module(services, value)

    def init_core(self, app):
        app.create("core")
        self.architect = Architect(app.core)
        self.composer = Composer(app.core, self.search.results)

    def add_handlers(self, app):
        chans = app.services.channels
        embed = app.services.intelligence.embedding
        comp = self.composer.compose
        select = self.architect.select
        app.core.input = Handler(chans, embed, "input", "route")
        app.core.select = Handler(chans, embed, "route", "compose", select)
        app.core.compose = Handler(chans, embed, "compose", "composed", comp)
        app.core.output = Handler(chans, embed, "composed", "output")

    def add_routes(self):
        self.add_route("/ws", self.relay)
        self.add_route("/", RootResource())

    def start_tasks(self):
        asyncio.gather(asyncio.create_task(self.search.delete_all_docs("prompts")))
        asyncio.gather(asyncio.create_task(self.search.delete_all_docs("functions")))
        asyncio.gather(asyncio.create_task(self.search.load_indexes()))

    def _set_module(self, services, module_settings):
        name = module_settings.get("name")
        import_path = module_settings.get("import_path")
        settings = module_settings.get("settings")
        module = get_module(import_path, name)
        setattr(self, name.lower(), module(services, **settings))
