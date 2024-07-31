from typing import Any, Dict


class ContextTree:
    def __init__(self):
        self._context: Dict[str, Any] = {"global": {}, "actors": {}}

    def set_global(self, key: str, value: Any):
        self._context["global"][key] = value

    def get_global(self, key: str, default=None) -> Any:
        return self._context["global"].get(key, default)

    def set_actor_context(self, actor_id, key: str, value: Any):
        if actor_id not in self._context["actors"]:
            self._context["actors"][actor_id] = {}
        self._context["actors"][actor_id][key] = value

    def get_actor_context(self, actor_id, key: str, default=None) -> Any:
        return self._context["actors"].get(actor_id, {}).get(key, default)

    def get_full_context(self, actor_id) -> Dict[str, Any]:
        context = self._context["global"].copy()
        context.update(self._context["actors"].get(actor_id, {}))
        return context
