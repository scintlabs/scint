from __future__ import annotations

from scint.lib.compose import ContextDescriptor
from scint.lib.exchange import Publishable, Subscribable
from scint.lib.observability import Observable, Observant
from scint.lib.context import Channel
from scint.lib.types import Processor
from scint.lib.types.types import Extension
from scint.lib.types import Traits


class Name(Extension):
    context = ContextDescriptor()
    traits = Traits(Observable, Observant, Publishable, Subscribable)
    processor = Processor()
    handlers = {}
    channels: Channel = {}
