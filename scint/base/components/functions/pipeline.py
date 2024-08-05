from .function import FunctionData


class Pipeline:
    def __init__(self, *functions: FunctionData):
        self.functions = functions

    async def execute(self, llm_service, *args, **kwargs):
        result = None
        for function in self.functions:
            llm_representation = function.to_llm_representation()
            llm_args = await llm_service.generate_arguments(llm_representation, result)

            function_call = FunctionData(name=function.name, arguments=llm_args)
            result = await self.invoke_function(function, function_call)

        return result

    async def invoke_function(
        self, function: FunctionData, function_call: FunctionData
    ):
        method = getattr(function.callable, function.name)
        result = await method(**function_call.arguments)

        if hasattr(result, "__aiter__"):
            return [message async for message in result]
        return result
