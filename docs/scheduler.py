# from scint.base.modules.components.decorators import metadata
# from scint.base.modules.components.module import Module
# from scint.base.modules.components.relay import Relay
# from scint.support.types import ContextSnapshot, Message, RouteArguments, SystemMessage
# from scint.support.logging import log
#
# import subprocess
# from datetime import datetime
#
#
# class Reminders(Relay):
#     """
#     The reminders Routine is for managing reminders and tasks.
#
#     Use the functions in this Routine to manage reminders and tasks.
#     """
#
#     @metadata(
#         description="Use this function to list the reminders in a specified list. If no list is provided, the default list is used.",
#         props={
#             "list_name": {
#                 "type": "string",
#                 "description": "The name of the reminders list to display.",
#             }
#         },
#     )
#     async def get_reminders(self, list_name: str = None):
#
#         applescript = """
#         tell application "Reminders"
#             set output to ""
#             repeat with r in reminders
#                 if completed of r is false then
#                     set output to output & name of r & " due by " & due date of r & linefeed
#                 end if
#             end repeat
#             return output
#         end tell
#         """
#
#         result = subprocess.run(
#             ["osascript", "-e", applescript], capture_output=True, text=True
#         )
#
#         yield SystemMessage(content=result.stdout.strip())
#
#
# class Calendar(Relay):
#     """
#     The calendar Routine is for managing calendar events and appointments.
#
#     Use the functions in this Routine to manage calendar events and appointments.
#     """
#
#     @metadata(
#         description="Use the create event function to add a new event to the calendar. If no date is provided, it creates an event 24 hours from the current time.",
#         props={
#             "title": {
#                 "type": "string",
#                 "description": "The summary or title of the event.",
#             },
#             "days": {
#                 "type": "integer",
#                 "description": "The number of days from the current date to the event start date.",
#             },
#             "hours": {
#                 "type": "integer",
#                 "description": "The hour of the event start time.",
#             },
#             "minutes": {
#                 "type": "integer",
#                 "description": "The minute of the event start time.",
#             },
#         },
#     )
#     async def new_event(
#         self, title: str, days: int = 1, hours: int = 0, minutes: int = 0
#     ):
#
#         calendar = "Calendar"
#         summary = (
#             f"make new event with properties "
#             + "{summary: "
#             + f'"{title}"'
#             + ", start date:theStartDate, end date:theEndDate}"
#         )
#
#         applescript = f"""
#             set theStartDate to (current date) + ({days} * days)
#             set hours of theStartDate to {hours}
#             set minutes of theStartDate to {minutes}
#             set seconds of theStartDate to 0
#             set theEndDate to theStartDate + (1 * hours)
#
#             tell application "Calendar"
#                 tell calendar "{calendar}"
#                     {summary}
#                     return "Event created successfully."
#                 end tell
#             end tell
#             """
#
#         result = subprocess.run(
#             ["osascript", "-e", applescript], capture_output=True, text=True
#         )
#
#         yield SystemMessage(content=result.stdout.strip())
#
#     @metadata(
#         description="Use this function to retrieve an event by date and title. If no title is provided, the default is used.",
#         props={
#             "title": {
#                 "type": "string",
#                 "description": "The summary or title of the event.",
#             },
#             "days": {
#                 "type": "integer",
#                 "description": "The number of days from the current date to the event start date.",
#             },
#             "hours": {
#                 "type": "integer",
#                 "description": "The hour of the event start time.",
#             },
#             "minutes": {
#                 "type": "integer",
#                 "description": "The minute of the event start time.",
#             },
#         },
#     )
#     async def get_event(self, title: str, days: int, hours: int = 0, minutes: int = 0):
#         date = datetime.strptime(date, "%Y-%m-%d")
#         applescript = f"""
#         set theStartDate to current date
#         set hours of theStartDate to 0
#         set minutes of theStartDate to 0
#         set seconds of theStartDate to 0
#         set theEndDate to theStartDate + (1 * days) - 1
#
#         tell application "Calendar"
#             tell calendar "Project Calendar"
#                 every event where its start date is greater than or equal to theStartDate and end date is less than or equal to theEndDate
#             end tell
#         end tell
#         """
#
#         result = subprocess.run(
#             ["osascript", "-e", applescript],
#             capture_output=True,
#             text=True,
#         )
#
#         yield SystemMessage(content=result.stdout)
#
#     @metadata(
#         description="Use the this function to list the upcoming events in the calendar for a specified time period. If no time period is provided, the default is used.",
#         props={
#             "days_ahead": {
#                 "type": "integer",
#                 "description": "Check calendar events for the specified days ahead.",
#             }
#         },
#     )
#     async def get_up_next(self, days_ahead: int = 1):
#
#         days = days_ahead.get("days_ahead", 1)
#         applescript = f"""
#         set theStartDate to current date
#         set hours of theStartDate to 0
#         set minutes of theStartDate to 0
#         set seconds of theStartDate to 0
#         set theEndDate to theStartDate + ({days} * days) - 1
#
#         tell application "Calendar"
#             tell calendar "Calendar"
#                 set theEvents to every event where its start date is greater than or equal to theStartDate and end date is less than or equal to theEndDate
#                 set output to ""
#                 repeat with theEvent in theEvents
#                     set output to output & "Event: " & title of theEvent & ", Start: " & start date of theEvent & ", End: " & end date of theEvent & linefeed
#                 end repeat
#                 return output
#             end tell
#         end tell
#         """
#
#         result = subprocess.run(
#             ["osascript", "-e", applescript],
#             capture_output=True,
#             text=True,
#         )
#
#         log.info(result)
#
#         yield SystemMessage(content=result.stdout)
#
#
# class Scheduler(Module):
#     """
#     The schedule relay provides tools and functions for managing schedules, reminders, appointments, and events.
#
#     Use the functions in this relay to manage schedules, reminders, appointments, and events.
#     """
#
#     relays = [Reminders(), Calendar()]
#     function_choice = {"type": "function", "function": {"name": "route"}}
#
#     async def parse(self, message: Message):
#         log.info(f"{self.name} received message.")
#         self.messages.append(message)
#         async for response in self.intelligence.parse(ContextSnapshot(**self.metadata)):
#             if isinstance(response, RouteArguments):
#                 log.info(f"Routing message {response}.")
#                 res = response.content
#                 relay = res.get("relay")
#                 log.info(f"Relay: {relay}")
#
#                 async for route_res in self.route.call(relay=relay, message=message):
#                     log.info(f"Routing to {relay}.")
#                     yield route_res
#
#             elif isinstance(response, Message):
#                 log.info(f"Returning response.")
#                 yield response
#
#     @metadata(
#         f"Use this function to route messages to the appropriate module.",
#         {
#             "relay": {
#                 "type": "string",
#                 "description": "Select an available relay to process the request.",
#                 "enum": [relay.name for relay in relays],
#             },
#         },
#     )
#     async def route(self, relay: str = None, message=None):
#         if relay:
#             re = next((r for r in Scheduler.relays if r.name == relay), None)
#             async for response in re.parse(message):
#                 yield response
