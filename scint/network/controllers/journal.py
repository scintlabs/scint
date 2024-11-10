import asyncio
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import wraps
from typing import Any, Dict, List, Optional


class EventCategory(Enum):
    SYSTEM = "system"
    USER = "user"
    PROCESS = "process"
    DATA = "state"
    ERROR = "error"
    INFO = "error"


class EventPriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


@dataclass
class Event:
    id: str
    timestamp: datetime
    category: EventCategory
    priority: EventPriority = EventPriority.NORMAL
    metadata: Dict[str, Any] = None
    parent_event_id: Optional[str] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class Journal:
    def __init__(self):
        self.events: List[Event] = []
        self.handlers: Dict[type, List[callable]] = {}

    def record(func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                name = func.__qualname__.split(".")[0]
                func_name = func.__name__
                top_level = len(self._call_stack) == 0
                self._call_stack.append(func_name)
                if top_level:
                    if func_name == "__init__":
                        event = dict(name=name, data=f"Initializing {name}.")
                    else:
                        event = dict(
                            name=func_name,
                            data=f"{name} called {' -> '.join(self._call_stack)}.",
                            arguments={"args": args, "kwargs": kwargs},
                        )
                    self.state.collect(event)

                try:

                    result = await func(self, *args, **kwargs)
                    if top_level:
                        event = dict(
                            name=func_name,
                            data=" -> ".join(self._call_stack),
                            result=str(result) if result else None,
                        )
                        self.state.collect(event)
                    return result
                except BaseException as e:
                    print(f"Exception in {' -> '.join(self._call_stack)}: {e}")
                    raise
                finally:
                    self._call_stack.pop()

        else:

            @wraps(func)
            def wrapper(self, *args, **kwargs):
                name = func.__qualname__.split(".")[0]
                func_name = func.__name__
                top_level = len(self._call_stack) == 0
                self._call_stack.append(func_name)
                if top_level:
                    if func_name == "__init__":
                        event = dict(name=name, data=f"Initializing {name}.")
                    else:
                        event = dict(
                            name=func_name,
                            data=f"{name} called {' -> '.join(self._call_stack)}.",
                            arguments={"args": args, "kwargs": kwargs},
                        )
                    self.state.collect(event)

                try:
                    result = func(self, *args, **kwargs)
                    if top_level:
                        event = dict(
                            name=func_name,
                            data=" -> ".join(self._call_stack),
                            result=str(result) if result else None,
                        )
                        self.state.collect(event)
                    return result
                except BaseException as e:
                    print(f"Exception in {' -> '.join(self._call_stack)}: {e}")
                    raise
                finally:
                    self._call_stack.pop()

        return wrapper

    def create_event(self, event_type: type, **kwargs) -> Event:
        event_id = str(uuid.uuid4())
        timestamp = datetime.now()
        event = event_type(id=event_id, timestamp=timestamp, **kwargs)
        self.process_event(event)
        return event

    def process_event(self, event: Event):
        self.events.append(event)
        event_type = type(event)
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                handler(event)

    def register_handler(self, event_type: type, handler: callable):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
