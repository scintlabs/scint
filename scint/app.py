from __future__ import annotations

from scint.base import Server
from scint.base.components.emitters.interface import Interface

server = Server()
server.add_route("/ws", server.services.messagebus)

interface = Interface()
