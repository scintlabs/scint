from scint.core.tools import Tool, Tools
from scint.core.worker import Worker
from scint.services.logger import log


class CreateEvent(Tool):
    name = "create_event"
    description = "Use this function to create reminders."
    props = {
        "name": {
            "type": "string",
            "description": ".",
        },
        "year": {
            "type": "integer",
            "description": "The 4-digit year.",
        },
        "month": {
            "type": "integer",
            "description": "The 2-digit month.",
        },
        "day": {
            "type": "integer",
            "description": "The 2-digit day.",
        },
        "time": {
            "type": "string",
            "description": "The time of the event, if applicable.",
        },
        "alarm": {
            "type": "boolean",
            "description": "Return true to set an alarm for the given day and time.",
        },
    }
    required = ["name", "year", "month", "day"]


class GetEvents(Tool):
    name = "get_events"
    description = (
        "Use this function to return a list of scheduled events and reminders."
    )
    props = {
        "get_future_events": {
            "type": "boolean",
            "description": "Return true to see a list of all future scheduled events.",
        },
        "get_past_events": {
            "type": "boolean",
            "description": "Return true to see a list of all previously scheduled events.",
        },
    }
    required = []


class Planner(Worker):
    def __init__(self):
        super().__init__()
        self.name = "Planner"
        self.tools = Tools()

        self.tools.add(CreateEvent())
        self.tools.add(GetEvents())

        log.info(f"{self.name} loaded.")
