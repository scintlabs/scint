import os
import asyncio
import subprocess
from datetime import datetime

from scint.modules.components.module import Module
from scint.modules.components.scope import Scope
from scint.support.types import Message, SystemMessage
from scint.system.logging import log


class App(Module):
    """
    This module encapsulates and manages all available modules and scopes.

    You are the main module for Scint. You manage all available modules and scopes by routing messages and requests to the appropriate destination.
    """

    async def select_component(self, component_name: str, message: Message, **kwargs):
        description = "Use this function to select the appropriate component for the message or request."
        props = {
            "component_name": {
                "type": "string",
                "description": "The name of the scope to switch to.",
                "enum": ["Data", "Schedule", "System"],
            }
        }

        for component in self.modules + self.scopes:
            if component.name == component_name:
                log.info(f"Forwarding message to {component.name}.")
                async for response in component.parse(message):
                    if isinstance(response, SystemMessage):
                        yield response

    class Data(Module):
        """
        This module provides tools and functions for managing data, including storage, retrieval, and manipulation.

        Use the functions in this module to manage data, including storage, retrieval, and manipulation.
        """

        async def select_component(self, component_name: str, message: Message):
            self.description = "Use this function to select the appropriate component for the message or request."
            self.props = {
                "component_name": {
                    "type": "string",
                    "description": "The name of the scope to switch to.",
                    "enum": ["FileSystem"],
                }
            }

            for component in self.modules + self.scopes:
                if component.name == component_name:
                    log.info(f"Forwarding message to {component.name}.")
                    async for response in component.parse(message):
                        if isinstance(response, SystemMessage):
                            yield response

        class FileSystem(Scope):
            """
            The FileSystem scope is for accessing data and information on the local filesystem.

            Use the functions in this scope to access data and information on the local filesystem.
            """

            async def list_data(self, path: str = None):
                description = "Use this function to list th contents of a specified path. If no path is provided, the root directory is used."
                props = {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list data from.",
                    }
                }

                base_path = "/Users/kaechle/Developer"
                data_list = []

                for item in os.listdir(base_path):
                    item_path = os.path.join(base_path, item)
                    if os.path.isdir(item_path):
                        data_list.append(f"[DIR] {item}")

                    else:
                        data_list.append(f"[FILE] {item}")

                if not data_list:
                    data_list.append("No files or directories found.")

                list = "\n".join(data_list)
                yield SystemMessage(content=f"The requested data: {list}")

    class Scheduler(Module):
        """
        The schedule module provides tools and functions for managing schedules, reminders, appointments, and events.

        Use the functions in this module to manage schedules, reminders, appointments, and events.
        """

        async def select_component(self, component_name: str, message: Message):
            description = "Use this function to select the appropriate component for the message or request."
            props = {
                "component_name": {
                    "type": "string",
                    "description": "The name of the scope to switch to.",
                    "enum": ["Reminders", "Calendar"],
                }
            }

            for component in self.modules + self.scopes:
                if component.name == component_name:
                    log.info(f"Forwarding message to {component.name}.")
                    async for response in component.parse(message):
                        if isinstance(response, SystemMessage):
                            yield response

        class Reminders(Scope):
            """
            The reminders scope is for managing reminders and tasks.

            Use the functions in this scope to manage reminders and tasks.
            """

            async def get_reminders(self, list_name: str = None):
                description = "Use this function to list the reminders in a specified list. If no list is provided, the default list is used."
                props = {
                    "list_name": {
                        "type": "string",
                        "description": "The name of the reminders list to display.",
                    }
                }

                applescript = """
                tell application "Reminders"
                    set output to ""
                    repeat with r in reminders
                        if completed of r is false then
                            set output to output & name of r & " due by " & due date of r & linefeed
                        end if
                    end repeat
                    return output
                end tell
                """

                result = subprocess.run(
                    ["osascript", "-e", applescript], capture_output=True, text=True
                )

                yield SystemMessage(content=result.stdout.strip())

        class Calendar(Scope):
            """
            The calendar scope is for managing calendar events and appointments.

            Use the functions in this scope to manage calendar events and appointments.
            """

            async def new_event(
                self, title: str, days: int = 1, hours: int = 0, minutes: int = 0
            ):
                description = "Use the create event function to add a new event to the calendar. If no date is provided, it creates an event 24 hours from the current time."
                props = {
                    "title": {
                        "type": "string",
                        "description": "The summary or title of the event.",
                    },
                    "days": {
                        "type": "integer",
                        "description": "The number of days from the current date to the event start date.",
                    },
                    "hours": {
                        "type": "integer",
                        "description": "The hour of the event start time.",
                    },
                    "minutes": {
                        "type": "integer",
                        "description": "The minute of the event start time.",
                    },
                }

                calendar = "Calendar"
                summary = (
                    f"make new event with properties "
                    + "{summary: "
                    + f'"{title}"'
                    + ", start date:theStartDate, end date:theEndDate}"
                )

                applescript = f"""
                    set theStartDate to (current date) + ({days} * days)
                    set hours of theStartDate to {hours}
                    set minutes of theStartDate to {minutes}
                    set seconds of theStartDate to 0
                    set theEndDate to theStartDate + (1 * hours)

                    tell application "Calendar"
                        tell calendar "{calendar}"
                            {summary}
                            return "Event created successfully."
                        end tell
                    end tell
                    """

                result = subprocess.run(
                    ["osascript", "-e", applescript], capture_output=True, text=True
                )

                yield SystemMessage(content=result.stdout.strip())

            async def get_event(
                self, title: str, days: int, hours: int = 0, minutes: int = 0
            ):
                description = "Use this function to retrieve an event by date and title. If no title is provided, the default is used."
                props = {
                    "title": {
                        "type": "string",
                        "description": "The summary or title of the event.",
                    },
                    "days": {
                        "type": "integer",
                        "description": "The number of days from the current date to the event start date.",
                    },
                    "hours": {
                        "type": "integer",
                        "description": "The hour of the event start time.",
                    },
                    "minutes": {
                        "type": "integer",
                        "description": "The minute of the event start time.",
                    },
                }

                date = datetime.strptime(date, "%Y-%m-%d")
                applescript = f"""
                set theStartDate to current date
                set hours of theStartDate to 0
                set minutes of theStartDate to 0
                set seconds of theStartDate to 0
                set theEndDate to theStartDate + (1 * days) - 1

                tell application "Calendar"
                    tell calendar "Project Calendar"
                        every event where its start date is greater than or equal to theStartDate and end date is less than or equal to theEndDate
                    end tell
                end tell
                """

                result = subprocess.run(
                    ["osascript", "-e", applescript],
                    capture_output=True,
                    text=True,
                )

                yield SystemMessage(content=result.stdout)

            async def get_up_next(self, days_ahead: int = 1):
                description = "Use the this function to list the upcoming events in the calendar for a specified time period. If no time period is provided, the default is used."
                props = {
                    "days_ahead": {
                        "type": "integer",
                        "description": "Check calendar events for the specified days ahead.",
                    }
                }

                days = days_ahead.get("days_ahead", 1)
                applescript = f"""
                set theStartDate to current date
                set hours of theStartDate to 0
                set minutes of theStartDate to 0
                set seconds of theStartDate to 0
                set theEndDate to theStartDate + ({days} * days) - 1

                tell application "Calendar"
                    tell calendar "Calendar"
                        set theEvents to every event where its start date is greater than or equal to theStartDate and end date is less than or equal to theEndDate
                        set output to ""
                        repeat with theEvent in theEvents
                            set output to output & "Event: " & title of theEvent & ", Start: " & start date of theEvent & ", End: " & end date of theEvent & linefeed
                        end repeat
                        return output
                    end tell
                end tell
                """

                result = subprocess.run(
                    ["osascript", "-e", applescript],
                    capture_output=True,
                    text=True,
                )

                log.info(result)

                yield SystemMessage(content=result.stdout)

    class System(Module):
        """
        This interface provides system tools and functions for accessing local and remote systems, troubleshooting, and more.

        Use the functions in this module to access system tools and functions for troubleshooting, maintenance, and more.
        """

        async def select_component(self, component_name: str, message: Message):
            description = "Use this function to select the appropriate component for the message or request."
            props = {
                "component_name": {
                    "type": "string",
                    "description": "The name of the scope to switch to.",
                    "enum": ["Commands"],
                }
            }

            for component in self.modules + self.scopes:
                if component.name == component_name:
                    log.info(f"Forwarding message to {component.name}.")
                    async for response in component.parse(message):
                        if isinstance(response, SystemMessage):
                            yield response

                else:
                    yield SystemMessage(content=f"Module {component_name} not found.")

        class Commands(Scope):
            """
            This scope provides terminal tools and functions for running UNIX terminal commands.

            Use the functions in this scope to run UNIX terminal commands from a macOS terminal with full sudo privileges.
            """

            async def use_terminal(self, commands: str):
                description = "Use this function to run UNIX terminal commands from a macOS terminal with full sudo privileges."
                props = {
                    "commands": {
                        "type": "string",
                        "description": "The UNIX terminal command to execute.",
                    }
                }

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
