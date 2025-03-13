from __future__ import annotations


from types import FunctionType
from typing import Any, Dict, List, Union
import urllib

from src.types.agents import Function, Output, Prompt, Routine, AgentSchema
from src.types.models import Model


def encode_obj(text: str, max_len: int = 30) -> str:
    text = text[:max_len]
    return urllib.parse.quote_plus(text)


def functions_from_dict(data: List[FunctionType]) -> List[Function]:
    functions = []
    for function in data:
        functions.append(Function(function))
    return functions


def routine_from_dict(data: FunctionType) -> Routine:
    return Routine(function=data)


def prompts_from_dict(data: List[Dict]) -> List[Prompt]:
    prompts = []
    for prompt in data:
        prompts.append(Prompt(**prompt))
    return prompts


def output_from_dict(data: Union[Model, Dict[str, Any]]) -> Output:
    return Output(format=data)


def agent_from_dict(data: Dict[str, Any]) -> AgentSchema:
    prompts = prompts_from_dict(data.get("prompts"))
    output = output_from_dict(data.get("output"))
    functions = functions_from_dict(data.get("functions"))
    routine_obj = routine_from_dict(data.get("routine"))

    return AgentSchema(
        prompts=prompts, output=output, functions=functions, routine=routine_obj
    )
