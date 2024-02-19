import json
from logging import config
from typing import List

import injector

from scint.components.config import Configuration, Preset
from scint.components.context import Context, ContextModule, IContextProvider
from scint.components.models import AssistantMessage, Message
from scint.components.tool import IToolsProvider, Tools, ToolsModule
from scint.services import openai_api
from scint.utils.logger import log


class Instance:
    def __init__(self, name, id, config, preset, description, context, tools, classref):
        self.name = name
        self.id = id
        self.config = config
        self.preset = preset
        self.prompt = description
        self.context: Context = context
        self.tools: Tools = tools
        self.classref = classref

    def get_state(self):
        log.info(f"Getting {self.name} state.")
        state = {
            "model": self.config.get("model", "default-model"),
            "temperature": self.config.get("temperature", 0.5),
            "top_p": self.config.get("top_p", 1),
            "frequency_penalty": self.config.get("frequency_penalty", 0),
            "presence_penalty": self.config.get("presence_penalty", 0),
            "messages": self.context.model_dump(),
            "tools": self.tools.model_dump(),
        }

        return state


class ICoreProvider:
    def register(self, name, id, preset, tooling, description):
        pass

    def get_process_state(self, name):
        pass

    async def generate_response(self, message):
        pass

    async def generate_tool_call(self, message):
        pass

    async def generate_embedding(self, message):
        pass


class CoreProvider(ICoreProvider):
    @injector.inject
    def __init__(self):
        self.instances: List[Instance] = []
        context_provider_module = injector.Injector([ContextModule()])
        tools_provider_instance = injector.Injector([ToolsModule()])
        self.context_provider = context_provider_module.get(IContextProvider)
        self.tools_provider = tools_provider_instance.get(IToolsProvider)

    def register(self, name, id, preset, description, tooling, classref):
        log.info(f"Registering {name}.")
        preset = preset if preset else Preset.process
        description = description if description else None
        tools = self.tools_provider.register(name, tooling) if tooling else None
        context = (
            self.context_provider.register(name, description) if description else None
        )
        config = Configuration.build(Preset=preset)
        self.instances.append(
            Instance(
                name=name,
                id=id,
                config=config,
                preset=preset,
                description=description,
                context=context,
                tools=tools,
                classref=classref,
            )
        )

    # def get_process(self, process_name):
    #     for instance in self.instances:
    #         if instance.name == process_name:
    #             return instance.class_ref()

    #     raise ValueError(f"Classname {process_name} not registered")

    def get_process_state(self, process_name):
        log.info(f"Getting {process_name} instance.")
        for instance in self.instances:
            if instance.name == process_name:
                return instance

        return None

    def get_process_instance(self, classname):
        for instance in self.instances:
            if instance.name == classname:
                return instance.classref()

        raise ValueError(f"Classname {classname} not registered.")

    async def generate_response(self, message: Message):
        instance = self.get_process_state(message.receiver)
        instance.messages.append(message)
        instance_state = instance.get_state()
        try:
            async for response in openai_api.chat_completion(**instance_state):
                if response is not None:
                    reply = AssistantMessage(
                        content=response, sender=instance.name, receiver="User"
                    )
                    instance.messages.append(reply)
                    yield reply

        except Exception as e:
            log.error(e)
            yield

    async def generate_tool_call(self, message: Message):
        log.info(f"Generating tool call with {message.receiver} for {message.sender}.")
        process = self.get_process_state(message.receiver)
        process.context.add_message(message)
        try:
            async for tool_calls in openai_api.tool_completion(**process.get_state()):
                if tool_calls is not None:
                    try:
                        for tool_call in tool_calls:
                            function = tool_call.get("function")
                            tool_name = function.get("name")
                            tool_args = json.loads(function.get("arguments"))
                            tool = process.tools.get_tool(tool_name)
                            async for result in tool.function(**tool_args):
                                process.context.add_message(message)
                                yield result

                    except Exception as e:
                        log.error(f"{e} while generating tool call.")

        except Exception as e:
            log.error(f"{e} while generating tool call.")

    async def generate_embedding(self, message: Message):
        try:
            result = await openai_api.embedding(message)
            yield result

        except Exception as e:
            log.error(f"Error generating embedding: {e}")
            raise


class CoreModule(injector.Module):
    @injector.provider
    def core_provider(self) -> ICoreProvider:
        return CoreProvider()

    def configure(self, binder: injector.Binder) -> None:
        binder.bind(ICoreProvider, to=self.core_provider)
