from __future__ import annotations


class State:
    def __init__(self, initial_value, persistence_key=None):
        self.initial_value = initial_value
        self.persistence_key = persistence_key
        self.private_name = None

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if not hasattr(instance, self.private_name):
            value = self._load_state() or self.initial_value
            setattr(instance, self.private_name, value)
        return getattr(instance, self.private_name)

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)
        if self.persistence_key is not None:
            self._save_state(value)

    def _save_state(self, value):
        print(f"Persisting {self.persistence_key} = {value}")
        with open(f"{self.persistence_key}.txt", "w") as f:
            f.write(str(value))

    def _load_state(self):
        try:
            with open(f"{self.persistence_key}.txt", "r") as f:
                data = f.read()
                print(f"Loaded persisted {self.persistence_key} = {data}")
                return data
        except FileNotFoundError:
            return None
