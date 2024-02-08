import json
from datetime import datetime
from typing import Dict, List
from deltron.constants import CONFIG

from deltron.data.pipeline import SystemMessage
from deltron.agents import SelectSearchResult, SummarizeData, Workers
from deltron.services.openai import completion
from deltron.utils.logger import log


class ProcessMeta(type):
    def __new__(cls, name, bases, dct):
        base_config = CONFIG
        config = {**base_config, **dct.pop("config", {})}
        dct["config"] = config

        return super().__new__(cls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.name = cls.__name__
        instance.config = {**cls.config, **kwargs.get("config", {})}
        instance.workers = Workers()
        instance.initialize_workers()

        return instance


class Process(metaclass=ProcessMeta):
    instructions = None

    def get_state(self, message) -> Dict[str, any]:
        if not isinstance(message, SystemMessage):
            message = SystemMessage(content=message)

        messages = [message.data_dump()]

        return {
            "model": self.config.get("model"),
            "temperature": self.config.get("temperature"),
            "top_p": self.config.get("top_p"),
            "max_tokens": self.config.get("max_tokens"),
            "presence_penalty": self.config.get("presence_penalty"),
            "frequency_penalty": self.config.get("frequency_penalty"),
            "messages": messages,
            "tools": self.workers.data_dump(),
            "tool_choice": self.config.get("worker_choice"),
        }

    async def call(self, message):
        try:
            state = self.get_state(message)
            async for worker_calls in completion(**state):
                for worker_call in worker_calls:
                    function = worker_call.get("function")
                    worker_name = function.get("name")
                    func_args = json.loads(function.get("arguments"))
                    async for response in self.eval_function_call(
                        worker_name, **func_args
                    ):
                        yield response

        except Exception as e:
            log.error(f"{self.name} {e}")
            raise

    async def eval_function_call(self, worker_name, **func_args):
        log.info(f"Evaluating function call from {self.__class__.__name__}.")
        worker = self.workers.get(worker_name)
        if worker is not None:
            try:
                async for response in worker.function(**func_args):
                    yield response

            except Exception as e:
                log.error(f"{self.name}: {e}")
                raise


class Processes:
    def __init__(self, processes: List[Process] = None):
        if processes is None:
            processes = []

        self._processes = processes

    def __iter__(self):
        return iter(self._processes)

    def load(self, *processes):
        for process in processes:
            if process.name not in [p.name for p in self._processes]:
                self._processes.append(process)

    def unload(self, process_name):
        self._processes = [
            process for process in self._processes if process.name != process_name
        ]

    def get(self, process_name):
        return next(
            (process for process in self._processes if process.name == process_name),
            None,
        )


class Select(Process):
    instructions = "You are a web search selection process. For every message, select the website that best matches the search query."

    def initialize_workers(self):
        self.workers.add(SelectSearchResult())


class Load(Process):
    instructions = "You are a website loading process. For every message, load the appropriate data for the search query."

    def initialize_workers(self):
        pass


class Parse(Process):
    instructions = "You are a data parsing process. For every message you receive, generate a contextually rich summary."

    def initialize_workers(self):
        self.workers.add(SummarizeData())
