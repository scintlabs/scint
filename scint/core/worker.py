from typing import Dict

from scint import config
from scint.core.component import Component


class Worker(Component):
    def __init__(self):
        self.name = "Worker"
        self.identity = f"You are a {self.name} module for Scint."
        self.instructions = ""
        self.config = config.DEFAULT_CONFIG

    def get_tools(self):
        tools = {}
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "tool_metadata"):
                tools[attr_name] = attr.tool_metadata
        return tools


class Workers:
    def __init__(self, workers: Dict[str, Worker] = {}):
        self._workers = workers

    def add(self, worker: Worker):
        self._workers[worker.name] = worker

    def remove(self, worker_name):
        if worker_name in self._workers:
            del self._workers[worker_name]

    def get_worker(self, worker_name):
        return self._workers.get(worker_name)
