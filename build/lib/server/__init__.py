from falcon.asgi.app import App as Falcon

from scint.server.root import RootResource


class Server(Falcon):
    def run(self, *args, **kwargs):
        self.create_server(*args, **kwargs)

    def create_server(self, *args, **kwargs):
        self.add_route("/", RootResource())
