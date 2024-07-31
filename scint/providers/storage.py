from scint.base.types.providers import ProviderType


class StorageProvider(metaclass=ProviderType):
    def __init__(self):
        super().__init__()
        self.context = None
