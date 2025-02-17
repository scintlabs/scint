from __future__ import annotations

from scint.api.types import Trait


class Loadable(Trait):
    def load(self, app, settings):
        with app as context:
            self.load_aspects(settings)
            self.load_channels(context)
            self.load_registry(context, settings)
            self.load_structure(context)

    def load_resource(self, context, settings): ...

    def set_module(self, context, module_settings): ...
