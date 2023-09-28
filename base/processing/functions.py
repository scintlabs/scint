from typing import List, Dict, Optional, Union, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, Json

from base.persistence import LifeCycle


class FunctionCall(BaseModel):
    name: str
    arguments: Json[dict]


class ParameterProperty(BaseModel):
    type: str
    description: str


class FunctionParameters(BaseModel):
    type: str = "object"
    properties: Dict[str, ParameterProperty]
    required: Optional[List[str]]


class OpenAIFunction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    lifecycle: LifeCycle
    name: str
    description: str
    parameters: FunctionParameters


def create_openai_function(
    name: str,
    description: str,
    properties: Dict[str, Union[str, Dict[str, Any]]],
    required: Optional[List[str]] = None,
) -> OpenAIFunction:
    from base.persistence import LifeCycle

    parameters_properties = {
        key: (
            ParameterProperty(**value)
            if isinstance(value, dict)
            else ParameterProperty(type=value, description="")
        )
        for key, value in properties.items()
    }
    function_parameters = FunctionParameters(
        properties=parameters_properties, required=required
    )
    lifecycle: LifeCycle = LifeCycle()
    return OpenAIFunction(
        name=name,
        description=description,
        parameters=function_parameters,
        lifecycle=lifecycle,
    )


async def eval_model_function(function_call):
    pass


initialize_entity = create_openai_function(
    name="initialize_entity",
    description="Use this function to initialize the different components and capabilities of Scint, including the Finder, Processor, and Generator.",
    properties={
        "entity": {
            "type": "string",
            "description": "The entity to use for the given task",
            "enum": ["Finder", "Processor", "Generator"],
        },
        "task": {
            "type": "string",
            "description": "The task.",
        },
    },
    required=["task", "entity"],
)

notify_agent = create_openai_function(
    name="agents",
    description="Use this function to communicate with the agents controlling Scint's systems, including its Coordinator and Sentry.",
    properties={
        "agent": {
            "type": "string",
            "description": "The agent being initialized.",
            "enum": ["Coordinator", "Sentry"],
        },
        "message": {
            "type": "string",
            "description": "The message to send to the specified agent.",
        },
    },
    required=["agent", "message"],
)
