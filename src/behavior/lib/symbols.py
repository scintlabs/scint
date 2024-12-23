from enum import Enum
from types import new_class

from src.processes.models import Function


class SymbolType(type):
    def __new__(cls, name, bases, dct, **kwds):
        return super().__new__(cls, name, bases, dct, **kwds)


class Symbols(Enum):
    function = {"model": Function}


async def new_symbol(symbol, name, desc, parameters, code, returns):
    kwds = {"metaclass": SymbolType}
    match Symbols(symbol):
        case Symbols.function:
            kwds.update(Symbols.function)

    return new_class(symbol, (), kwds, lambda ns: ns)() if kwds else None
