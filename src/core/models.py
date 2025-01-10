from __future__ import annotations

from functools import cached_property
from typing import Any, Dict, Type, TypeVar, Generic

from pydantic import create_model, BaseModel

from ..core.types import Aspect


T = TypeVar("T", bound=BaseModel)


class Modelable(Aspect, Generic[T]):
    model_config: Dict[str, Any] = {"extra": "forbid", "frozen": True}

    @property
    def model(self) -> Dict[str, Any]:
        raise NotImplementedError

    @cached_property
    def pydantic_model(self) -> Type[T]:
        model_dict = self.model

        def dict_to_pydantic(d: Dict[str, Any], name: str = "Model") -> Type[BaseModel]:
            fields = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    fields[key] = (
                        dict_to_pydantic(value, f"{name}{key.capitalize()}"),
                        ...,
                    )
                elif isinstance(value, list):
                    if value and isinstance(value[0], dict):
                        item_model = dict_to_pydantic(
                            value[0], f"{name}{key.capitalize()}Item"
                        )
                        fields[key] = (list[item_model], ...)
                    else:
                        fields[key] = (type(value), ...)
                else:
                    fields[key] = (type(value) if value is not None else Any, ...)

            return create_model(name, __config__=self.model_config, **fields)

        return dict_to_pydantic(model_dict, self.__class__.__name__ + "Model")

    def validate(self, data: Dict[str, Any]) -> T:
        return self.pydantic_model(**data)
