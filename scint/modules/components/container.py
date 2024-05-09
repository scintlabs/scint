import json
from scint.controllers.context import context_controller
from scint.support.types import Message
from scint.system.logging import log
import redis


class Container:
    def __init__(self, owner):
        self._context_controller = context_controller
        self._data = []
        self._owner = owner
        self._container_name = f"{owner.__class__.__name__}_{id(owner)}"
        self._context_controller.register(self._container_name, owner)
        self._redis = redis.Redis(host="localhost", port=6379, db=0)
        self._redis_key_prefix = f"{self._container_name}:"
        self._redis_ttl = 3600

    def append(self, message: Message):
        log.info(f"Appending message to {self._owner}'s container.")
        log.debug(f"{message}")

        self._data.append(message)
        message_id = str(id(message))
        redis_key = f"{self._redis_key_prefix}{message_id}"
        serialized_message = message.model_dump_json()
        self._redis.set(redis_key, serialized_message, ex=self._redis_ttl)

    def update_context(self, message: Message):
        self.update_context(self._container_name, self._owner, message)

    def rebuild_thread(self, context, search, keywords):
        log.info(f"Rebuilding thread with context, search, and keywords.")
        log.debug(f"{context}, {search}, {keywords}")

        self._data = self._context_controller.rebuild_thread(
            self._container_name, self._owner, context, search, keywords
        )
        redis_messages = self._get_messages_from_redis()
        rethinkdb_messages = self._context_controller.rebuild_thread(
            self._container_name, self._owner, context, search, keywords
        )
        self._data = redis_messages + rethinkdb_messages

    def _get_messages_from_redis(self):
        redis_keys = self._redis.keys(f"{self._redis_key_prefix}*")
        messages = []
        for key in redis_keys:
            serialized_message = self._redis.get(key)
            if serialized_message:
                message_dict = json.loads(serialized_message)
                message = Message(**message_dict)
                messages.append(message)
        return messages

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)
