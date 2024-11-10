from typing import Dict, Optional


class StateStore:
    def __init__(self):
        self.state: Dict[str, dict] = {}

    async def update(self, key: str, data: dict):
        if key not in self.state:
            self.state[key] = {}
        self.state[key].update(data)

    async def get(self, key: str) -> Optional[dict]:
        return self.state.get(key)
