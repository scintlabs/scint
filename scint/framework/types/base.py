from scint.framework.state.state import State, state
from scint.framework.state.metadata import collector


class BaseType(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        return {"name": name, "state": state(name)}

    def __new__(cls, name, bases, dct, **kwds):
        def _index(self):
            for key, value in self.state.items():
                print(key)

        def _parse(self, obj):
            for key, value in obj.items():
                if key == "labels" and value is not None:
                    self.labels.add(item for item in value)

        def _calculate(self, obj):
            for key, value in obj.items():
                if key == "embedding" and value is not None:
                    self.embeddings.append(value)
                    self.embedding = [sum(e) / len(e) for e in zip(self.embeddings)]

        dct["_type"] = kwds.get("type")
        dct["_index"] = _index
        dct["_parse"] = _parse
        dct["_calculate"] = _calculate
        dct["_call_stack"] = []
        for key, value in dct.items():
            if callable(value) and not key.startswith("__"):
                if callable(value):
                    dct[key] = collector(value)
                elif not isinstance(value, State):
                    dct[key] = State()

        return super().__new__(cls, name, bases, dct)
