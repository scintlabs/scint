from typing import Any, Callable, Dict, List

from scint.network.protocol.routes import Route
from scint.repository.models.struct import Struct


class Router(Struct):
    def __init__(self):
        self.routes: Dict[str, Route] = {}
        self.middleware: List[Callable] = []

    def route(self, path: str, method: str = "GET"):
        def decorator(handler: Callable):
            self.routes[f"{method}:{path}"] = Route(path, handler, method)
            return handler

        return decorator

    def middleware(self, middleware: Callable):
        self.middleware.append(middleware)
        return middleware


class RouteDispatcher:
    def __init__(self, router: Router):
        self.router = router

    async def dispatch(self, request):
        route = self.router.routes.get(f"{request.method}:{request.path}")
        if not route:
            raise Exception()

        context = await self.build_context(request, route)
        return await self.execute_route(context, route)

    async def build_context(self, request, route):
        pass

    async def execute_route(self, context, route):
        pass


class RouteContext:
    def __init__(self, request, params, state):
        self.request = request
        self.params = params
        self.state = state


class RouteBuilder:
    def __init__(self):
        self.routes = {}

    def add(self, path: str):
        def decorator(handler: Callable):
            self.routes[path] = handler
            return handler

        return decorator


class ProcessRouter(Router):
    def __init__(self):
        super().__init__()
        self.services = {}

    def register_service(self, name: str, service: Any):
        self.services[name] = service

    async def route_to_service(self, service: str, method: str, **kwargs):
        service = self.services.get(service)
        if not service:
            raise
        return await getattr(service, method)(**kwargs)


class MessageRouter:
    def __init__(self):
        self.handlers = {}
        self.channels = {}

    def on_message(self, channel: str):
        def decorator(handler: Callable):
            self.handlers[channel] = handler
            return handler

        return decorator

    async def route_message(self, message):
        handler = self.handlers.get(message.channel)
        if handler:
            await handler(message)


class Router:
    def __init__(self):
        self.middleware = None
        self.service_router = None
        self.process_router = None
        self.event_router = None

    def add_middleware(self, middleware: Callable):
        self.middleware.append(middleware)

    async def route(self, target_type: str, target: str, payload: Any, **kwargs):
        for middleware in self.middleware:
            payload = await middleware(payload)

        match target_type:
            case "service":
                return await self.service_router.route_to_service(
                    target, payload, **kwargs
                )
            case "process":
                return await self.process_router.route_to_process(target, payload)
            case "message":
                return await self.message_router.route_message(payload)
            case _:
                raise
