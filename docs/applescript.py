# import datetime
# import subprocess
#
# from scint.support.types import SystemMessage
# from scint.support.logging import log
#
#
# async def reminders_get_list(self, list_name: str = None):
#     applescript = """
#     tell application "Reminders"
#         set output to ""
#         repeat with r in reminders
#             if completed of r is false then
#                 set output to output & name of r & " due by " & due date of r & linefeed
#             end if
#         end repeat
#         return output
#     end tell
#     """
#
#     result = subprocess.run(
#         ["osascript", "-e", applescript], capture_output=True, text=True
#     )
#
#     yield SystemMessage(content=result.stdout.strip())
#
#
# async def calendar_new_event(title: str, days: int = 1, hours: int = 0, mins: int = 0):
#     calendar = "Calendar"
#     summary = (
#         f"make new event with properties "
#         + "{summary: "
#         + f'"{title}"'
#         + ", start date:theStartDate, end date:theEndDate}"
#     )
#
#     applescript = f"""
#         set theStartDate to (current date) + ({days} * days)
#         set hours of theStartDate to {hours}
#         set minutes of theStartDate to {mins}
#         set seconds of theStartDate to 0
#         set theEndDate to theStartDate + (1 * hours)
#
#         tell application "Calendar"
#             tell calendar "{calendar}"
#                 {summary}
#                 return "Event created successfully."
#             end tell
#         end tell
#         """
#
#     result = subprocess.run(
#         ["osascript", "-e", applescript], capture_output=True, text=True
#     )
#
#     yield SystemMessage(content=result.stdout.strip())
#
#
# async def calendar_find_event(title: str, days: int, hours: int = 0, mins: int = 0):
#     date = datetime.strptime(date, "%Y-%m-%d")
#     applescript = f"""
#     set theStartDate to current date
#     set hours of theStartDate to 0
#     set minutes of theStartDate to 0
#     set seconds of theStartDate to 0
#     set theEndDate to theStartDate + (1 * days) - 1
#
#     tell application "Calendar"
#         tell calendar "Project Calendar"
#             every event where its start date is greater than or equal to theStartDate and end date is less than or equal to theEndDate
#         end tell
#     end tell
#     """
#
#     result = subprocess.run(
#         ["osascript", "-e", applescript],
#         capture_output=True,
#         text=True,
#     )
#
#     yield SystemMessage(content=result.stdout)
#
#
# async def calendar_next_up(days_ahead: int = 1):
#     applescript = f"""
#     set theStartDate to current date
#     set hours of theStartDate to 0
#     set minutes of theStartDate to 0
#     set seconds of theStartDate to 0
#     set theEndDate to theStartDate + ({days_ahead} * days) - 1
#
#     tell application "Calendar"
#         tell calendar "Calendar"
#             set theEvents to every event where its start date is greater than or equal to theStartDate and end date is less than or equal to theEndDate
#             set output to ""
#             repeat with theEvent in theEvents
#                 set output to output & "Event: " & title of theEvent & ", Start: " & start date of theEvent & ", End: " & end date of theEvent & linefeed
#             end repeat
#             return output
#         end tell
#     end tell
#     """
#
#     result = subprocess.run(["osascript", "-e", applescript], capture_output=True)
#     yield SystemMessage(content=result.stdout)
