from __future__ import annotations

from falcon.asgi import App

from scint.base.types.library import Library
from scint.base.types.studio import Studio
from scint.base.types.context import Context

context = Context()
library = Library()
studio = Studio()

print(context.providers)
app = App()

app.add_route("/ws", context.providers.broker)
app.add_route("/search", context.providers.search)
