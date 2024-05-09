from scint.support.types import Any
from rethinkdb import RethinkDB

r = RethinkDB()


class ContextController:
    def __init__(self):
        self._containers = []
        self._rethinkdb_conn = r.connect("localhost", 28015)
        self._rethinkdb_db = "scint"
        self._rethinkdb_table = "messages"

    def register(self, name: str, owner: Any, parent: Any = None):
        container = {"name": name, "owner": owner, "parent": parent, "messages": []}
        self._containers.append(container)

    def get(self):
        return [container for container in self._containers]

    def update(self, container_name: str, message: Any):
        container = self._find_container(container_name)
        if container:
            container["messages"].append(message)

    def rebuild(
        self,
        container_name: str,
        owner: Any,
        context: dict,
        search: str,
        keywords: list,
    ):
        container = self._find_container(container_name)
        if container and container["owner"] == owner:
            rebuilt_messages = []
            for message in container["messages"]:
                if (
                    self._match_context(message, context)
                    and self._match_search(message, search)
                    and self._match_keywords(message, keywords)
                ):
                    rebuilt_messages.append(message)
            container["messages"] = rebuilt_messages
            return rebuilt_messages
        return []

    def sync_messages_to_rethinkdb(self):
        for container in self._containers:
            container_name = container["name"]
            redis_messages = self._get_expired_messages_from_redis(container_name)
            self._store_messages_in_rethinkdb(container_name, redis_messages)

    def _find_container(self, name: str):
        for container in self._containers:
            if container["name"] == name:
                return container
        return None

    def _get_expired_messages_from_redis(self, container_name):
        # Implement logic to retrieve expired messages from Redis for the given container
        # Return the list of expired messages
        pass

    def _store_messages_in_rethinkdb(self, container_name, messages):
        # Implement logic to store messages in RethinkDB for the given container
        pass

    def _match_context(self, message: Any, context: dict):
        # Implement logic to match message with the given context
        # Return True if the message matches the context, False otherwise
        pass

    def _match_search(self, message: Any, search: str):
        # Implement logic to match message with the given search query
        # Return True if the message matches the search query, False otherwise
        pass

    def _match_keywords(self, message: Any, keywords: list):
        # Implement logic to match message with the given keywords
        # Return True if the message matches any of the keywords, False otherwise
        pass


context_controller = ContextController()
