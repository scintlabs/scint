from __future__ import annotations

from typing import Callable, Dict, List, Set, Any
from threading import Lock
import logging

from scint.lib.schema.threads import Event
from scint.lib.common.traits import Trait

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_observers: Dict[str, Set[Callable]] = {}
_observer_lock = Lock()


class Directory:
    def __init__(self):
        self.entries: Dict[str, DirectoryEntry] = {}
        self.events: Dict[str, List[Event]] = {}

    def add_entry(self, obj: Any):
        self.entries[obj.id] = DirectoryEntry(object_id=obj.id, object_ref=obj)

    def get_entry(self, obj_id: str) -> DirectoryEntry:
        return self.directory[obj_id]

    def remove_entry(self, obj_id: str) -> None:
        if obj_id not in self.entries:
            raise KeyError(f"Entry {obj_id} not found")
        del self.entries[obj_id]

    def add_event(self, event: Event):
        self.events[event.event_type].append(event)


class DirectoryEntry:
    object_id: str
    object_ref: Any
    events: List[Event] = []


class Observant(Trait):
    def subscribe(event_type: str, observer_fn: Callable) -> bool: ...


class Observable(Trait):
    def subscribe(event_type: str, observer_fn: Callable) -> bool:
        if not callable(observer_fn):
            logger.error(f"Observer must be callable: {observer_fn}")
            return False

        with _observer_lock:
            if event_type not in _observers:
                _observers[event_type] = set()

            _observers[event_type].add(observer_fn)
            logger.info(f"Observer {observer_fn.__name__} subscribed to {event_type}")
            return True

    def unsubscribe(event_type: str, observer_fn: Callable) -> bool:
        with _observer_lock:
            if event_type not in _observers:
                logger.warning(f"No observers found for event type: {event_type}")
                return False

            if observer_fn in _observers[event_type]:
                _observers[event_type].remove(observer_fn)
                logger.info(
                    f"Observer {observer_fn.__name__} unsubscribed from {event_type}"
                )

                if not _observers[event_type]:
                    del _observers[event_type]
                return True

            logger.warning(
                f"Observer {observer_fn.__name__} not found for event type: {event_type}"
            )
            return False

    def notify(event_type: str, *args, **kwargs) -> None:
        with _observer_lock:
            if event_type not in _observers:
                logger.debug(f"No observers for event type: {event_type}")
                return

            observers = list(_observers[event_type])

        for observer in observers:
            try:
                observer(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error notifying observer {observer.__name__}: {str(e)}")

    def clear_observers() -> None:
        with _observer_lock:
            _observers.clear()
            logger.info("All observers cleared")


# if __name__ == "__main__":

#     def price_changed(new_price: float):
#         print(f"Price changed to: ${new_price:.2f}")

#     def stock_alert(symbol: str, price: float):
#         print(f"Stock alert: {symbol} is now ${price:.2f}")

#     subscribe("price_update", price_changed)
#     subscribe("stock_alert", stock_alert)
#     notify("price_update", 99.99)
#     notify("stock_alert", "AAPL", 150.00)
#     unsubscribe("price_update", price_changed)
#     notify("price_update", 89.99)
#     clear_observers()
