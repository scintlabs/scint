from __future__ import annotations

from pprint import pp
from importlib import import_module
from typing import Any, Callable, Dict, List, Optional, Type

from src.types.models import Model
from src.types.structure import Struct, Trait
from src.util.helpers import (
    agent_from_dict,
    encode_obj,
    functions_from_dict,
    output_from_dict,
    prompts_from_dict,
    routine_from_dict,
)


class Module(Model):
    type: str
    base_path: str
    schema_path: str
    schema_type: Any


class Modules(Model):
    modules: List[Module]


class Composition(Trait):
    def load(self):
        modules = {
            "src.schemas.agents": ("AgentSchema", dict, "agents"),
            "src.schemas.components.routines": ("Routine", Callable, "routines"),
            "src.schemas.components.functions": ("Function", Callable, "functions"),
            "src.schemas.components.prompts": ("Prompt", dict, "prompts"),
            "src.schemas.components.outputs": ("Output", dict, "outputs"),
        }

        for path in modules.keys():
            module = import_module(path)
            cls_name, from_type, category = modules.get(path)
            for k, v in module.__dict__.items():
                if not k.startswith("_") and k.endswith(path.split(".")[-1][:-1]):
                    match path.split(".")[-1]:
                        case "agents":
                            cls = agent_from_dict(v)
                            self.register(cls, category)
                        case "routines":
                            cls = routine_from_dict([v])
                            self.register(cls, category)
                        case "functions":
                            cls = functions_from_dict([v])
                            self.register(cls, category)
                        case "prompts":
                            cls = prompts_from_dict([v])
                            self.register(cls, category)
                        case "outputs":
                            cls = output_from_dict(v)
                            self.register(cls, category)
                        case _:
                            pass

    def register(self, obj: Type, category: str):
        id = self.generate_id(obj)
        if not hasattr(self.components, category):
            self.components[category] = {}
        self.components[category][id] = obj
        pp(f"Registered component {id} => {obj}.")

    def unregister(self, id: str, category: str) -> None:
        if id in self.components.get(category, {}):
            del self.components[category][id]
            print(f"Unregistered {id} from {category}.")

    def lookup_component(self, id: str, category: str) -> Optional[Any]:
        return self.components.get(category, {}).get(id)

    def generate_id(self, obj: Any) -> str:
        parts = ["NS", "C"]
        class_name = obj.__class__.__name__
        class_name_encoded = encode_obj(class_name, 20)
        parts.append(f"CL:{class_name_encoded}")

        if hasattr(obj, "name") and obj.name:
            name_encoded = encode_obj(obj.name, 20)
            parts.append(f"N:{name_encoded}")

        return ":".join(parts)


class Library(Struct, traits=(Composition,)):
    components: Dict[str, Any] = {}
