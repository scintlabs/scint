from typing import Optional

from scint.base.utils import dictorial
from scint.base import settings

methods = ["completion", "image", "speech", "embedding"]
get_preset = lambda p: dictorial(settings, f"presets.{p}")
get_provider = lambda p: dictorial(f"support.{p}")


class Intelligence:
    def __init__(self, providers, presets):
        print("Starting intelligence service.")
        self._providers = providers
        self._presets = presets

    def get_preset(self, preset):
        return lambda preset: dictorial(self._presets, preset)

    def get_provider(self, provider: str, key: Optional[str] = None):
        return (
            get_provider(provider)
            if not key
            else dictorial(get_provider(provider), key)
        )
