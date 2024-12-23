from typing import Any, Optional

from ..types import StructType


class Resource(metaclass=StructType):
    def __init__(self, initial_data=None):
        self._data = {}
        if initial_data:
            self._data.update(initial_data)

    def load_resources(self, source_id: Optional[str] = None, **kwargs) -> None:
        pass

    def save_resources(self, destination_id: Optional[str] = None, **kwargs):
        pass

    def initialize(self):
        pass

    def finalize(self):
        pass

    def refresh(self):
        pass

    def get(self, key: str, default: Any = None):
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        self._data[key] = value

    def add(self, key: str, value: Any):
        pass

    def remove(self, key: str):
        if key in self._data:
            del self._data[key]

    def has(self, key: str):
        return key in self._data

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    def get_metadata(self, key: str) -> Optional[dict]:
        return None

    def get_schema(self, key: str) -> Optional[dict]:
        return None

    def __contains__(self, key: str) -> bool:
        return self.has(key)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        self.remove(key)
