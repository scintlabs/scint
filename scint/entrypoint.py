from scint.ensemble.composer import Composer
from scint.utils.helpers import set_module


def compose_context(settings=None, /, *args, **kwargs):
    class Composer:
        def __init__(self, settings=None, /, *args, **kwargs):
            super().__init__()

        def compose(self, settings, *args, **kwargs):
            for k, v in settings.as_dict().items():
                set_module(settings, v)
            self.settings = settings


def compose_ensemble(settings=None, /, *args, **kwargs):
    class Ensemble(Composer):
        def __init__(self, composer, settings=None, /, *args, **kwargs):
            super().__init__()

        def compose(self, settings, *args, **kwargs):
            self.load_processes(settings.processes)

        def load_processes(self, processes):
            pass


def compose_network(settings=None, /, *args, **kwargs):
    class Network(Composer):
        def __init__(self, settings=None, /, *args, **kwargs):
            super().__init__()

        def compose(self, settings, *args, **kwargs):
            for k, v in settings.mesh.as_dict().items():
                set_module(settings, v)
            self.settings = settings


def compose_state(settings=None, /, *args, **kwargs):
    class State(Composer):
        def __init__(self, settings=None, /, *args, **kwargs):
            super().__init__()

        def compose(self, settings, *args, **kwargs):
            for k, v in settings.mesh.as_dict().items():
                set_module(settings, v)
            self.settings = settings
