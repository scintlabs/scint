import asyncio
from scint.base.modules.components.decorators import metadata
from scint.base.modules.components.module import Module
from scint.base.modules.components.routine import Routine
from scint.support.types import SystemMessage


class Commands(Routine):
    """
    This Routine provides terminal tools and functions for running UNIX terminal commands.

    Use the functions in this Routine to run UNIX terminal commands from a macOS terminal with full sudo privileges.
    """

    @metadata(
        description="Use this function to run UNIX terminal commands from a macOS terminal with full sudo privileges.",
        props={
            "commands": {
                "type": "string",
                "description": "The UNIX terminal command to execute.",
            }
        },
    )
    async def use_terminal(self, commands: str):

        process = await asyncio.create_subprocess_shell(
            commands,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await process.communicate()
        output = stdout.decode().strip() if stdout else ""
        errors = stderr.decode().strip() if stderr else ""
        full_output = output + "\n" + errors if errors else output
        yield SystemMessage(content=full_output)


class System(Module):
    """
    This interface provides system tools and functions for accessing local and remote systems, troubleshooting, and more.

    Use the functions in this module to access system tools and functions for troubleshooting, maintenance, and more.
    """

    routines = [Commands()]
