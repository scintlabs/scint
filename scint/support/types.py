from typing import (
    Tuple,
    Dict,
    List,
    Optional,
    Callable,
    AsyncGenerator,
    Union,
    Any,
)

import websockets
from pydantic import BaseModel, Field, validator


WebSocket = websockets.WebSocketCommonProtocol
WebSocketDisconnect = websockets.exceptions.ConnectionClosed
