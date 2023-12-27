from scint import config
from scint.core.component import Component
from scint.core.messages import Message
from scint.core.worker import Workers
from scint.core.processing.archiver import Archiver
from scint.core.processing.composer import Composer
from scint.core.processing.planner import Planner
from scint.core.processing.researcher import Researcher
from scint.core.tools import Tool, Tools
from scint.services.logger import log


class Classifier(Tool):
    name = "classifier"
    description = "Use this function to classify messages for memory storage."
    props = {
        "request_type": {
            "type": "string",
            "description": "Use this paramater to classify the request by type.",
            "enum": ["general", "research", "task"],
        },
        "keyword": {
            "type": "string",
            "description": "If the topic changes, choose the closest appropriate keyword to classify the message.",
        },
        "named_entities": {
            "type": "array",
            "description": "List any named entities within the message.",
        },
    }
    required = ["request_type", "keyword", "named_entities"]

    async def classify(keyword, named_entities):
        pass


class InitializeWorker(Tool):
    description = "Use this function to initialize the appropriate worker based on the provided input."
    props = {
        "worker_required": {
            "type": "boolean",
            "description": "Return true if the request requires an available worker, otherwise return false.",
        },
        "worker": {
            "type": "string",
            "description": "The worker to assign the task to.",
            "enum": ["web_researcher"],
        },
        "task": {
            "type": "string",
            "description": "A clear description of the requested task.",
        },
    }
    required = ["worker_required"]

    async def initialize_worker(self, worker_required, worker=None, task=None):
        if worker_required is True:
            log.info(f"Processor: initializing {worker} to complete task.")

            try:
                command = Message(f"{task}", self.__class__.__name__)
                worker = self.workers.get_worker(worker)
                response = await worker.generate_response(command)
                return response

            except Exception as e:
                log.error(f"Error: {e}")

        else:
            log.info(f"Processor: no workers required.")
            return


class Processor(Component):
    def __init__(self):
        super().__init__()
        self.name = "Processor"
        self.identity = config.PROCESSOR
        self.instructions = config.PROCESSOR_INSTRUCTIONS
        self.config = config.PROCESSOR_CONFIG
        self.tools = Tools()

        log.info(f"{self.name} loaded, loading worker modules ...")

        self.workers = Workers()
        self.workers.add(Archiver())
        self.workers.add(Composer())
        self.workers.add(Planner())
        self.workers.add(Researcher())
