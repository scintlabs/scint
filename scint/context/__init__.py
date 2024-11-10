from scint.utils.helpers import set_module


def compose(self, settings, *args, **kwargs):
    for k, v in settings.as_dict().items():
        set_module(settings, v)
    self.settings = settings
