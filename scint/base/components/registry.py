from typing import Callable, Dict, Any, List
from dataclasses import dataclass, field


from ..behavior.strategies.build import (
    extract_function_metadata,
    extract_function_metadata,
    prepare_llm_input,
)
from scint.base.components.functions.schema import FunctionData


class FunctionDepot:
    def __init__(self):
        self.functions: Dict[str, FunctionData] = {}

    def register(self, func: Callable) -> None:
        metadata = extract_function_metadata(func)
        schema = FunctionData(
            name=metadata["name"],
            description=metadata["description"],
            parameters=metadata["parameters"],
            source=metadata["source"],
            callable=func,
        )
        self.functions[metadata["name"]] = schema

    def get_function(self, name: str) -> FunctionData:
        """Retrieve a function schema by name."""
        return self.functions.get(name)

    def get_all_functions(self) -> List[FunctionData]:
        """Retrieve all registered function schemas."""
        return list(self.functions.values())

    def to_llm_representation(self) -> List[Dict[str, Any]]:
        """Convert all registered functions to LLM-friendly representation."""
        return [prepare_llm_input(func.callable) for func in self.functions.values()]

    async def execute(self, function_name: str, *args, **kwargs):
        """Execute a registered function by name."""
        function = self.get_function(function_name)
        if not function:
            raise ValueError(f"Function '{function_name}' not found.")

        result = await function.callable(*args, **kwargs)

        if hasattr(result, "__aiter__"):
            return [message async for message in result]
        return result
