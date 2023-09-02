from pydantic import BaseModel


# Model Definitions
class ChatMessage(BaseModel):
    message: str


class Command(BaseModel):
    command: str
    data: str


class StateMessage(BaseModel):
    state: str


class Observation(BaseModel):
    observe: str
