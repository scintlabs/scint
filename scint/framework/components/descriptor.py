from typing import Any, Dict


class Descriptor:
    def __set_name__(name):
        pass

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                return Descriptor(value)
            return value
        raise AttributeError(f"'ConfigNode' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def as_dict(self) -> Dict[str, Any]:
        return self._data
