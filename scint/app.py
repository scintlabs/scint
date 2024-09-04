from __future__ import annotations

from scint.core.orchestration import Orchestration
from scint.core.settings import Settings


def start():
    settings = Settings()
    app = Orchestration(settings)
    return app
