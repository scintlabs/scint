from scint.modules.components.module import Module
from scint.modules.components.scope import Scope
from scint.support.types import Message, SystemMessage
from scint.system.logging import log


class Schedule(Module):
    """
    description = "The schedule module provides tools and functions for managing schedules, reminders, appointments, and events."

    Use the functions in this module to manage schedules, reminders, appointments, and events.
    """

    async def select_scope(self, scope_name: str, message: Message):
        description = "This function selects a scope to use."
        props = {
            "scope_name": {
                "type": "string",
                "description": "The scope to switch to.",
                "enum": ["Calendar", "Reminders"],
            },
        }

        for scope in self.scopes:
            if scope.name == scope_name:
                log.info(f"Forwarding message to {scope}.")
                async for response in scope.parse(message):
                    yield response

            else:
                yield SystemMessage(content=f"Scope {scope_name} not found.")

    class Reminders(Scope):
        """
        The reminders scope is for managing reminders and tasks.

        Use the functions in this scope to manage reminders and tasks.
        """

        async def list_reminders(self, list_name: str = None):
            description = "Use this function to list the reminders in a specified list. If no list is provided, the default list is used."
            props = {
                "list_name": {
                    "type": "string",
                    "description": "The name of the reminders list to display.",
                }
            }

            yield SystemMessage(content="Listing reminders...")

    class Calendar(Scope):
        """
        The FileSystem scope is for accessing data and information on the local filesystem.

        Use the functions in this scope to access data and information on the local filesystem.
        """

        async def check_calendar(self, time_ahead: int = None):
            description = "Use the check calendar function to list the events in the calendar for a specified time period. If no time period is provided, the default is used."
            props = {
                "time_ahead": {
                    "type": "integer",
                    "description": "The time period to use.",
                }
            }

            yield SystemMessage(content="Listing calendar events...")
