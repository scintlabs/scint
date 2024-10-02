from falcon.asgi.app import App as Routes

from scint.framework.models.events import Event
from scint.framework.models.messages import (
    InputMessage,
    Message,
    OutputMessage,
    SystemMessage,
)
from scint.framework.entities.controller import Controller
from scint.framework.entities.coordinator import Coordinator
from scint.framework.entities.registry import Registry
from scint.framework.utils.helpers import get_module
from scint.app.presentation.root import RootResource
from scint.framework.base import Settings
from scint.app.core.router import Switch


class App:
    def __init__(self, scope, *args, **kwargs):
        self.scope = scope
        self.scope.print()


class Launcher(Coordinator):
    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings if settings else Settings()
        self.create_app()

    def create_app(self):
        with self.state as app:
            self.load_context(app)
            self.load_services(app)
            self.load_archive(app)
            self.load_engine(app)
            self.load_routes(app)
            self.app = App(app)

    def load_context(self, app):
        app.create("context")
        components = [Event, Message, InputMessage, OutputMessage, SystemMessage]
        app.context.components = Registry("components", *components)
        app.context.switch = Switch(app)

    def load_archive(self, app):
        app.archive = Controller(app)

    def load_engine(self, app):
        app.engine = Controller(app)

    def load_services(self, app):
        services = app.create("services")
        for key, value in self.settings.services.as_dict().items():
            self.set_module(services, value)

    def load_routes(self, app):
        app.routes = Routes()
        app.routes.add_route("/ws", app.services.broker)
        app.routes.add_route("/", RootResource())

    def set_module(self, services, module_settings):
        name = module_settings.get("name")
        import_path = module_settings.get("import_path")
        settings = module_settings.get("settings")
        module = get_module(import_path, name)
        setattr(services, name.lower(), module(services, **settings))
