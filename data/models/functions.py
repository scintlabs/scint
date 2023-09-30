from typing import List

from pydantic import BaseModel, Field


async def eval_model_function(function_call):
    pass


class Property(BaseModel):
    type: str
    description: str
    enum: List[str] = Field(default_factory=list)


class Properties(BaseModel):
    task: Property
    entity: Property


class Parameters(BaseModel):
    type: str
    properties: Properties


class ModelFunction(BaseModel):
    name: str
    description: str
    parameters: Parameters
    required: List[str]
