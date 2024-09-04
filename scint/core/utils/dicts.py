import functools
import json

from pydantic import BaseModel


__all__ = "dictorial", "keyfob"


def dictorial(data, attr):
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

        return functools.reduce(_getattr, [obj] + attr.split("."))

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


def keyfob(data, attr):
    def search_nested(obj, attr):
        if isinstance(obj, dict):
            if attr in obj:
                return obj[attr]
            for key, value in obj.items():
                result = search_nested(value, attr)
                if result is not None:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = search_nested(item, attr)
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
        result = search_nested(data, attr)
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
