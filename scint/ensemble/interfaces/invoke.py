from typing import Type, TypedDict


async def invoke(self, name: str, type_def, **kwargs) -> Type:
    attributes = {**type_def.attributes, **kwargs}
    for key, value in type_def.validators.items():
        if key in attributes:
            value(attributes[key])

    return type(name, (type_def.base,), TypedDict(**attributes))
