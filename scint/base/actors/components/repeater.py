class RepeaterType(type):
    def __new__(cls, name, bases, attrs):
        return super().__new__(cls, name, bases, attrs)

    def __call__(cls, *functions):
        instance = cls.__new__(cls)
        instance.__init__(*functions)
        return instance


class Repeater(metaclass=RepeaterType):
    def __init__(self, *functions):
        self.functions = functions

    async def __call__(self, *args, **kwargs):
        result = None
        for function in self.functions:
            if result:
                kwargs["previous_result"] = result
            result = await self.execute_function(function, *args, **kwargs)
        return result

    async def execute_function(self, function, *args, **kwargs):
        request = function.build()
        arguments = await function.invoke(request)
        method = getattr(function, function.name)
        result = await method(**arguments)
        if hasattr(result, "__aiter__"):
            messages = []
            async for message in result:
                messages.append(message)
            return messages

        return result
