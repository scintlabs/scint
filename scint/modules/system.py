import asyncio
from scint.modules.components.module import Module
from scint.modules.components.scope import Scope
from scint.support.types import Message, SystemMessage


class System(Module):
    """
    This interface provides system tools and functions for accessing local and remote systems, troubleshooting, and more.

    Use the functions in this module to access system tools and functions for troubleshooting, maintenance, and more.
    """

    async def set_scope(self, scope_name: str):
        description = "This function switches between different scopes and contexts."
        props = {
            "scope_name": {
                "type": "string",
                "description": "The scope to switch to.",
                "enum": ["Maintenance"],
            },
        }

        for scope in self.scopes:
            if scope.name == scope_name:
                self.scopes_active.append(scope)

            yield SystemMessage(content=f"{scope_name} active, inform the user.")
        yield SystemMessage(content=f"Scope {scope_name} not found.")

    class Maintenance(Scope):
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


class Settings(Module):
    description = "This module provides tools and functions for managing user and system settings."
    instructions = [
        "You are the Settings module for Scint. You can manage user and system settings."
    ]

    async def set_scope(self, scope_name: str):
        description = "This function switches between different scopes and contexts."
        props = {
            "scope_name": {
                "type": "string",
                "description": "The scope to switch to.",
                "enum": ["Maintenance"],
            },
        }

        for scope in self.scopes:
            if scope.name == scope_name:
                self.scopes_active.append(scope)

            yield SystemMessage(content=f"{scope_name} active, inform the user.")
        yield SystemMessage(content=f"Scope {scope_name} not found.")

    class Maintenance(Scope):
        description = "This scope provides terminal tools and functions for running UNIX terminal commands."
        instructions = []

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


class Search(Module):
    """
    This module enables external search functionality for the web, local files and documents, and internal history.

    You are Scint, a dynamic system powered by artificial intelligence. You have access to the tools and knowledge to expand your capabilities, but pay close attention to guidelines as they shift depending on your currently active scheme and context.
    """

    async def set_scope(self, scope_name: str):
        description = "This function switches between different scopes and contexts."
        props = {
            "scope_name": {
                "type": "string",
                "description": "The scope to switch to.",
                "enum": ["Web", "Files"],
            },
        }

        for scope in self.scopes:
            if scope.name == scope_name:
                self.scopes_active.append(scope)

            yield SystemMessage(content=f"{scope_name} active, inform the user.")
        yield SystemMessage(content=f"Scope {scope_name} not found.")

    class Web(Scope):
        description = "This scope provides web search tools and functions for accessing external search engines, APIs, and databases."
        instructions = []

        async def search(self, query: str):
            description = "Use this function to search the web."
            props = {
                "query": {
                    "type": "string",
                    "description": "The search query to execute.",
                }
            }

            yield Message(role="system", content=query)

    class Files(Scope):
        description = "This scope provides file search tools and functions for accessing local files and documents."
        instructions = []

        async def search(self, query: str):
            description = "Use this function to search for files on the local system."
            props = {
                "query": {
                    "type": "string",
                    "description": "The search query to execute.",
                }
            }

            yield Message(role="system", content=query)


class Schedule(Module):
    description = "This module enables scheduling and automation functionality for the system. It can create, manage, and execute schedules for various tasks and functions."
    instructions = [
        "You are the Scheduler for Scint. You can create, manage, and execute schedules for various tasks and functions. Pay close attention to guidelines as they shift depending on your currently active scope and context."
    ]

    async def set_scope(self, scope_name: str):
        description = "This function switches between different scopes and contexts."
        props = {
            "scope_name": {
                "type": "string",
                "description": "The scope to switch to.",
                "enum": ["SystemTools"],
            },
        }

        for scope in self.scopes:
            if scope.name == scope_name:
                self.scopes_active.append(scope)

            yield SystemMessage(content=f"{scope_name} active, inform the user.")
        yield SystemMessage(content=f"Scope {scope_name} not found.")

    class Calendars(Scope):
        description = "This scope provides calendar tools and functions for managing schedules, events, and appointments."
        instructions = [
            "You are the Calendar scope for Scint. You can create, manage, and execute schedules for various tasks and functions. Pay close attention to guidelines as they shift depending on your currently active scope and context."
        ]

        async def create(self, name: str):
            description = "Use this function to create a new event in the calendar."
            props = {
                "name": {
                    "type": "string",
                    "description": "The name of the event to create.",
                }
            }

            yield Message(role="system", content=name)

    class Reminders(Scope):
        description = "This scope provides reminder tools and functions for managing reminders, notifications, and alerts."
        instructions = [
            "You are the Reminder scope for Scint. You can create, manage, and execute reminders for various tasks and functions. Pay close attention to guidelines as they shift depending on your currently active scope and context."
        ]

        async def create(self, name: str):
            description = "Use this function to create a new reminder."
            props = {
                "name": {
                    "type": "string",
                    "description": "The name of the reminder to create.",
                }
            }

            yield Message(role="system", content=name)


class Record(Module):
    description = "This model enables various tools for recording and storing data. It can create, manage, update, and delete entries for various purposes."
    instructions = [
        "You are the Recorder for Scint. You can create, manage, update, and delete entries for various purposes."
    ]

    async def set_scope(self, scope_name: str):
        description = "This function switches between different scopes and contexts."
        props = {
            "scope_name": {
                "type": "string",
                "description": "The scope to switch to.",
                "enum": ["SystemTools"],
            },
        }

        for scope in self.scopes:
            if scope.name == scope_name:
                self.scopes_active.append(scope)

            yield SystemMessage(content=f"{scope_name} active, inform the user.")
        yield SystemMessage(content=f"Scope {scope_name} not found.")

    class Notes(Scope):
        description = "This scope provides tools and functions for managing notes."
        instructions = [
            "You are the Notes scope for Scint. You can create, manage, and update notes for various purposes."
        ]

        async def list_notes(self, directory: str = None):
            description = "Use this function to list notes. Provide a directory to list notes in a specific folder, otherwise the function returns a full list."
            props = {
                "directory": {
                    "type": "string",
                    "description": "The specific directory to list, if any.",
                },
            }

        async def create(self, name: str):
            description = "Use this function to create a new note."
            props = {
                "name": {
                    "type": "string",
                    "description": "The name of the note to create.",
                },
                "content": {
                    "type": "string",
                    "description": "The content of the note.",
                },
            }

            yield SystemMessage(content=name)


class Parse(Module):
    description = "This module adds parsing functionality, allowing the system to process and interpet large volumes of text and data, such as code, documents, and more."
    instructions = [
        "You are the Parser for Scint. You can process and interpret large volumes of text and data, such as code, documents, and more. Pay close attention to guidelines as they shift depending on your currently active scope and context."
    ]

    async def set_scope(self, scope_name: str):
        description = "This function switches between different scopes and contexts."
        props = {
            "scope_name": {
                "type": "string",
                "description": "The scope to switch to.",
                "enum": ["Code", "Documents", "Data"],
            },
        }

        for scope in self.scopes:
            if scope.name == scope_name:
                self.scopes_active.append(scope)

            yield SystemMessage(content=f"{scope_name} active, inform the user.")
        yield SystemMessage(content=f"Scope {scope_name} not found.")

    class Code(Scope):
        description = "This scope provides code parsing tools and functions for processing and interpreting code, scripts, and programming languages."
        instructions = []

        async def map_codebase(self, link: str):
            description = "Use this function to map a codebase for analysis."
            props = {
                "link": {
                    "type": "string",
                    "description": "The URL or path to the codebase to map.",
                }
            }

            yield Message(role="system", content=link)

    class Documents(Scope):
        description = "This scope provides document parsing tools and functions for processing and interpreting documents, articles, and text files."
        instructions = []

        async def read(self, link: str):
            description = "Use this function to read and parse a document."
            props = {
                "link": {
                    "type": "string",
                    "description": "The URL or path to the document to read.",
                }
            }

            yield Message(role="system", content=link)
