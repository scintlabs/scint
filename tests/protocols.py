from typing import Protocol, Dict, List, Any

from scint.core.primitives.messages import Message
from scint.core import Construct


class Index: ...


class Sketch: ...


class Categorical(Protocol):
    def sketch(self) -> Sketch: ...
    def construct(self) -> Construct: ...
    def index(self) -> Index: ...


class Sketchable(Protocol):
    def index(self) -> Index: ...


class Indexable(Protocol):
    def sketch(self) -> Sketch: ...
    def construct(self) -> Construct: ...


class Constructable(Protocol):
    def index(self) -> Index: ...


class Subscribable(Protocol):
    async def subscribe(self, channel) -> Message: ...


class Publishable(Protocol):
    async def publish(self, channel: Subscribable, message: Message) -> None: ...


class Persistable(Protocol):
    async def follow(self) -> List[Any]: ...
    async def unfollow(self) -> None: ...


class Browsable(Protocol):
    async def browse(self) -> Dict[str, str]: ...


class Parsable(Protocol):
    async def parse(self) -> Any: ...


class Mappable(Protocol):
    async def parse(self) -> Any: ...
