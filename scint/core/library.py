import importlib
import uuid

from scint.support.logging import log


class Library:
    def __init__(self, data):
        self.data = data

    def load_module(self, module_path):
        return importlib.import_module(module_path)

    def load_config(self, config):
        self.data = config.copy()
        for module_name, details in self.core.items():
            self.modules[module_name] = details.get("import")
            categories = details.get("categories")
            for category in categories:
                categories[category] = []
        self.load_data()

    def load_data(self):
        for key, value in self.data:
            for item in value:
                item["id"] = str(uuid.uuid4())

    def read(self, module):
        data = []
        for item in self.data[module]:
            data.append(item)
        return data
