from scint.repository.models.base import Trait


class Inspect(Trait):
    def model(self):
        dct = {}
        for k, v in self.__dict__.items():
            try:
                dct[k] = v.model
            except AttributeError:
                if isinstance(v, list):
                    dct[k] = [i.model for i in v]
                elif isinstance(v, dict):
                    dct[k] = {k: v.__dict__ for k, v in self.__dict__.items()}
                elif isinstance(v, str):
                    dct[k] = v
            return dct
