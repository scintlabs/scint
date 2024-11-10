from falcon.asgi.app import App as Routes

from scint.api.endpoints.ws import WebsocketResource
from scint.api.middleware import __all__


def create_routes():
    return Routes(middleware=[m() for m in __all__])


routes = create_routes()
routes.add_route("/ws", WebsocketResource())
