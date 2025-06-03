import json
import os
import importlib
import importlib.resources as pkg_resources
from functools import reduce
from typing import Any, Dict, List

import yaml
from attrs import define


@define
class SettingsNode:
    _data: Dict[str, Any]

    def __getattr__(self, name: str):
        if name in self._data:
            value = self._data[name]
            if isinstance(value, dict):
                return SettingsNode(value)
            return value
        raise AttributeError(f"'ConfigNode' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any):
        if name == "_data":
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def as_dict(self) -> Dict[str, Any]:
        return self._data


@define
class Settings:
    _settings: Dict[str, Any] = {}
    _load_order: List[str] = []

    def __attrs_post_init__(self):
        self.load_json("settings/services.json", "services")

    def load_json(self, file_path: str, namespace: str = ""):
        with open(file_path, "r") as f:
            data = json.load(f)
        self._merge_settings(data, namespace)
        self._load_order.append(f"JSON:{file_path}:{namespace}")

    def load_yaml(self, file_path: str, namespace: str = ""):
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        self._merge_settings(data, namespace)
        self._load_order.append(f"YAML:{file_path}:{namespace}")

    def load_env(self, prefix: str = "SCINT_", namespace: str = ""):
        env_settings = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                env_key = key[len(prefix) :].lower()
                env_settings[env_key] = self._parse_value(value)
        self._merge_settings(env_settings, namespace)
        self._load_order.append(f"ENV:{prefix}:{namespace}")

    def load_package_resource(self, pkg: str, src: str, ns: str = ""):
        content = pkg_resources.read_text(pkg, src)
        if src.endswith(".yaml") or src.endswith(".yml"):
            data = yaml.safe_load(content)
        elif src.endswith(".json"):
            data = json.loads(content)
        else:
            raise ValueError(f"Unsupported resource type: {src}")
        self._merge_settings(data, ns)
        self._load_order.append(f"RESOURCE:{pkg}:{src}:{ns}")

    def load_module(self, module_name: str, namespace: str = ""):
        module = importlib.import_module(module_name)
        module_settings = {
            k: v for k, v in module.__dict__.items() if not k.startswith("_")
        }
        self._merge_settings(module_settings, namespace)
        self._load_order.append(f"MODULE:{module_name}:{namespace}")

    def _parse_value(self, value: str) -> Any:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def get(self, key: str, default: Any = None) -> Any:
        try:
            return reduce(lambda d, k: d[k], key.split("."), self._settings)
        except (KeyError, TypeError):
            return default

    def as_dict(self) -> Dict[str, Any]:
        return self._settings.copy()

    def get_load_order(self) -> List[str]:
        return self._load_order.copy()

    def __getattr__(self, name: str) -> Any:
        if name in self._settings:
            value = self._settings[name]
            if isinstance(value, dict):
                return SettingsNode(value)
            return value
        raise AttributeError(f"'Settings' object has no attribute '{name}'")

    def _merge_settings(self, data: Dict[str, Any], namespace: str):
        if namespace:
            keys = namespace.split(".")
            current = self._settings
            for key in keys[:-1]:
                current = current.setdefault(key, {})
            current[keys[-1]] = self._deep_merge(current.get(keys[-1], {}), data)
        else:
            self._settings = self._deep_merge(self._settings, data)

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]):
        for key, value in override.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
