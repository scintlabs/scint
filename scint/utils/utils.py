import inspect
import json
from functools import partial, reduce, wraps

from pydantic import BaseModel


from scint.repository.models.base import Model
from scint.repository.models.struct import Struct
from scint.utils.monads import Maybe


def unbind(method, self):
    original_func = method.__func__
    return partial(original_func, self)


def bind(func):
    @wraps(func)
    def method_wrapper(self, *args, **kwargs):
        return func(*args, **kwargs)


def build_function(func, wrapper=None, binder=None):
    return Struct(
        callable=wrapper(binder) if binder is not None else wrapper(func),
        model=Struct(
            name=func.__name__,
            description=inspect.getdoc(func),
            parameters=inspect.signature(func).parameters,
        ),
    )


def unpack(object, paths):
    for p in paths:
        n = p.split(".")[-1]
        d = p(object, p)

        result = (
            Maybe.unit(d)
            .bind(lambda d: unpack_invocations(d) if n == "tool_calls" else Maybe(d))
            .bind(lambda d: unpack_composition(d) if n == "content" else Maybe(d))
            .bind(lambda d: unpack_embedding(d) if n == "embedding" else Maybe(d))
            .bind(create_invocation if n == "tool_calls" else Maybe.unit)
            .bind(create_message if n == "content" else Maybe.unit)
            .bind(create_embedding if n == "embedding" else Maybe.unit)
        )

        if result.value is not None:
            return result.value

    return None


def unpack_invocations(data):
    return Maybe.unit(c for c in extract(data, "tool_calls"))


def unpack_composition(data):
    return Maybe.unit(extract(data, "content"))


def unpack_embedding(data):
    return Maybe.unit(extract(data, "embedding"))


def create_invocation(data):
    return Maybe.unit(Model.select("Message")(**json.loads(data)))


def create_message(data):
    return Maybe.unit(Model.select("Message")(**json.loads(data)))


def create_embedding(data):
    return Maybe.unit({"path": "scint", "store": extract_nested(data, "embedding")})


def extract(data, attr):
    def rgetattr(obj, attr):
        def _getattr(obj, attr):
            try:
                if isinstance(obj, dict):
                    return obj[attr]
                if isinstance(obj, list):
                    return obj[int(attr)]
                return getattr(obj, attr)
            except (KeyError, IndexError, AttributeError, ValueError):
                return None

        return reduce(_getattr, [obj] + attr.split("."))

    try:
        result = rgetattr(data, attr)
        if result is not None:
            return result
        if isinstance(data, dict) and attr in data:
            return data[attr]
        if isinstance(data, str):
            try:
                json_data = json.loads(data)
                if attr in json_data:
                    return json_data.get(attr)
            except json.JSONDecodeError:
                pass
    except (KeyError, IndexError, AttributeError):
        pass
    return None


def extract_nested(data, attr):
    def _nested(obj, attr):
        if isinstance(obj, dict):
            if attr in obj:
                return obj[attr]
            for key, value in obj.items():
                result = _nested(value, attr)
                if result is not None:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = _nested(item, attr)
                if result is not None:
                    return result
        else:
            if hasattr(obj, attr):
                return getattr(obj, attr)
            if isinstance(obj, BaseModel):
                try:
                    return obj.model_model().get(attr)
                except AttributeError:
                    pass
        return None

    try:
        result = _nested(data, attr)
        if result is not None:
            return result
        if isinstance(data, dict) and attr in data:
            return data[attr]
        if isinstance(data, BaseModel):
            try:
                return data.model_model().get(attr)
            except AttributeError:
                pass
        if isinstance(data, str):
            try:
                json_data = json.loads(data)
                if attr in json_data:
                    return json_data.get(attr)
            except json.JSONDecodeError:
                pass
    except (KeyError, IndexError, AttributeError):
        pass
    return None


__all__ = extract, extract_nested, unpack, create_embedding
