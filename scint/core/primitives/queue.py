import json
from typing import Any, Dict, Optional

import redis.asyncio

from scint.core.components import Primitive


class Queue(Primitive):
    def __init__(self, other):
        self.name = other.pid
        self.store = redis.from_url("redis://localhost")

    def enqueue(self, message: Dict[str, Any]) -> bool:
        with self.context():
            try:
                self.store.lpush(self.name, json.dumps(message))
                return True
            except (TypeError, ValueError) as e:
                print(f"Failed to enqueue message: {e}")
                return False

    def dequeue(self) -> Optional[Dict[str, Any]]:
        with self.execution_context():
            message = self.store.rpop(self.name)
            if message:
                try:
                    return json.loads(message)
                except json.JSONDecodeError as e:
                    print(f"Failed to decode message: {e}")
                    return None
            return None

    def parse_command(self, message: Dict[str, Any]) -> Any:
        command_type = message.get("type")
        if command_type == "api_call":
            return ApiCommand(message)
        elif command_type == "internal_process":
            return InternalCommand(message)
        else:
            raise ValueError(f"Unknown command type: {command_type}")


class ApiCommand:
    def __init__(self, data):
        self.data = data


class InternalCommand:
    def __init__(self, data):
        self.data = data
