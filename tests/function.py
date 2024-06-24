import asyncio

from scint.support.logging import log
from scint.intelligence.requests import invoke

commands = [
    {
        "instructions": [
            {
                "content": "You are Scint, an artificial intelligence system designed to communicate and interact with a macOS system terminal as a natural language interface. Respond to commands and perform accordingly.",
            }
        ],
        "functions": [
            {
                "name": "use_terminal",
                "description": "Executes shell commands asynchronously and captures the output. Useful for running system commands or scripts from within the application.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute. Execute multiple commands by separating each with a semicolon.",
                        }
                    },
                    "required": ["command"],
                },
            }
        ],
        "context": [
            {"content": "Hello there."},
        ],
    }
]


class Invoker:
    def __init__(self, metafunctions):
        self.metafunctions = metafunctions
        self.context = []

    async def invoke(self):
        context = await self.build_context(await self.use_terminal("date; printenv"))
        res = await invoke(self.commands)
        log.info(res.arguments)
        return await self.use_terminal(**res.arguments)

    async def use_terminal(self, command: str):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() if stdout else ""
        errors = stderr.decode().strip() if stderr else ""
        full_output = output + "\n" + errors if errors else output
        return log.info(full_output)


invoker = Invoker()
asyncio.run(invoker.invoke())
