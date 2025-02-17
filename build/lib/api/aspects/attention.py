from __future__ import annotations

from pprint import pp

from scint.api.types import Aspect, Struct


class Attention(Aspect):
    def __init__(self, struct: Struct):
        struct.join(self)

    def focus(self, struct: Struct):
        struct.join(self)

    def __setitem__(self, key, value):
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key):
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)

    def get_map(self):
        def _map(obj):
            if isinstance(obj, Struct):
                return {k: _map(v) for k, v in obj.items() if not k.startswith("_")}
            elif isinstance(obj, dict) or issubclass(type(obj), dict):
                return {k: _map(v) for k, v in obj.items() if not k.startswith("_")}
            elif isinstance(obj, (list, tuple, set)):
                return [_map(item) for item in obj]

        return _map(self)

    def print(self):
        return pp(self.get_map())
