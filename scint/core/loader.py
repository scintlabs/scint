import importlib
import uuid

from scint.modules.logging import log


class Loader:
    def __init__(self):
        self.library = {
            "prompts": None,
            "functions": None,
            "people": None,
        }
        self.load()

    def load(self):
        for name, value in self.library.items():
            lib_module = importlib.import_module(f"scint.data.lib.{name}")
            if lib_module:
                lib_data = []
                lib_attr = getattr(lib_module, name)
                if isinstance(lib_attr, list):
                    for item in lib_attr:
                        if item.get("metadata"):
                            key = item["metadata"]
                            meta_item = getattr(lib_module, "metadata").get(key)
                            if meta_item.get("id") is None:
                                meta_item["id"] = str(uuid.uuid4())
                            lib_data.append(meta_item)
                        elif item.get("id") is None:
                            item["id"] = str(uuid.uuid4())
                            lib_data.append(item)
                self.library[name] = lib_data
        log.info(f"Library loaded.")

loader = Loader()


log.info(uuid.uuid4())
