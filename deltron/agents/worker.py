import inspect
from typing import Any, Dict, List, Optional

from deltron.data.pipeline import SystemMessage


class WorkerMeta(type):
    def __new__(cls, name, bases, dct):
        if "function" in dct:
            original_function = dct["function"]
            func_signature = inspect.signature(original_function)
            parameters = func_signature.parameters
            required_params = [
                param_name
                for param_name, param in parameters.items()
                if param.kind in (param.POSITIONAL_OR_KEYWORD, param.KEYWORD_ONLY) and param_name != "self"
            ]

        dct["name"] = name
        dct["metadata"] = cls.data_dump(name, dct, required_params)
        return super().__new__(cls, name, bases, dct)

    @classmethod
    def data_dump(cls, name, dct, required_params):
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": dct.get("description"),
                "parameters": {
                    "type": "object",
                    "properties": dct.get("props"),
                    "required": required_params,
                },
            },
        }


class Worker(metaclass=WorkerMeta):
    def __init__(self) -> None:
        self.description = None
        self.props = None

    async def function(self):
        raise NotImplementedError("This method should be overridden in the subclass.")


class Workers:
    def __init__(self, workers: Optional[List[Worker]] = None):
        self._workers = workers if workers is not None else []

    def __iter__(self):
        return iter(self._workers)

    def add(self, worker: Worker):
        if worker.name not in [t.name for t in self._workers]:
            self._workers.append(worker)

    def remove(self, worker_name: str):
        self._workers = [worker for worker in self._workers if worker.name != worker_name]

    def get(self, worker_name: str) -> Optional[Worker]:
        return next((worker for worker in self._workers if worker.name == worker_name), None)

    def data_dump(self) -> List[Dict[str, Any]]:
        return [worker.__class__.metadata for worker in self._workers]
