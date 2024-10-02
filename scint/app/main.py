import asyncio
from falcon.asgi.app import App as Server

from scint.app.core.router import Router
from scint.presentation.root import RootResource
from scint.framework.entities.controller import Controller
from scint.framework.entities.coordinator import Coordinator
from scint.framework.entities.interface import Interface
from scint.framework.entities.registry import Registry
from scint.framework.base.settings import Settings
from scint.framework.state.context import Context
from scint.framework.utils.helpers import get_module


class App(Interface):
    def __init__(self):
        self.server = Server()
        self.settings = Settings()
        self.launcher = Launcher()

    def start(self):
        self.launcher.create_app(self, self.settings)
        self.set_endpoints()
        self.context_view()

    def set_endpoints(self):
        self.server.add_route("/ws", self.context.services.broker)
        asyncio.gather(asyncio.create_task(self.context.services.broker.subscribe()))
        self.server.add_route("/", RootResource())

    def context_view(self, view=None):
        context = Context(self.state)
        context.print()


class Launcher(Coordinator):
    def __init__(self):
        super().__init__()

    def create_app(self, app, settings):
        with app.state as context:
            self.load_router(context)
            self.load_services(context, settings)
            self.load_composition(context)
            app.context = context

    def load_router(self, context):
        context.router = Router(context)

    def load_services(self, context, settings):
        services = context.create("services")
        services.registry = Registry(services, "services", ["scint.app.services"])
        for key, value in settings.services.as_dict().items():
            self.set_module(services, value)

    def load_composition(self, context):
        composition = context.create("composition")
        composition.components = Registry(
            composition, "components", ["scint.framework.components"]
        )
        composition.archive = Controller(composition)
        composition.engine = Controller(composition)

    def set_module(self, services, module_settings):
        name = module_settings.get("name")
        import_path = module_settings.get("import_path")
        settings = module_settings.get("settings")
        module = get_module(import_path, name)
        setattr(services, name.lower(), module(services, **settings))
