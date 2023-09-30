from pydantic import BaseModel


class Tag(BaseModel):
    tag: str
    description: str
