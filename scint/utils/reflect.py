from scint.repository.models.base import Trait 


class Reflect(Trait):
    def __init__(self):
        self.name = None
        self.description = None
        self.parameters = None

    def model_trait(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
                "strict": True,
            },
        }

    def model_struct(trait):
        @property
        def model(self):
            dict = {}
            for key, value in self.__dict__.items():
                try:
                    dict[key] = value.model
                except AttributeError:
                    dict[key] = value
