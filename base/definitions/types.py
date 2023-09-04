from enum import Enum
from pydantic import BaseModel


# Model Definitions
class UserRequest(BaseModel):
    message: str


class SystemMessage(BaseModel):
    message: str
