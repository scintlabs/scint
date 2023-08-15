import subprocess

main = [
    {
        "name": "response",
        "description": "Use this function for every message you send and receive.",
        "parameters": {
            "user_message_summary": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The path to the directory the file is located.",
                    }
                },
            },
            "assistant_response": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The path to the directory the file is located.",
                    }
                },
            },
            "assistant_response_summary": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The path to the directory the file is located.",
                    }
                },
            },
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The path to the directory the file is located.",
                },
                "filepath": {
                    "type": "string",
                    "description": "The full path to the file",
                },
            },
            "required": ["filepath"],
        },
    },
]

files = [
    {
        "name": "open_file",
        "description": "Retrieve one of the files you have access to.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The path to the directory the file is located.",
                },
                "filepath": {
                    "type": "string",
                    "description": "The full path to the file",
                },
            },
            "required": ["filepath"],
        },
    },
    {
        "name": "share_file",
        "description": "Share a link to a file that you can send to other contacts.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file.",
                },
                "filepath": {
                    "type": "string",
                    "description": "The full path to the directory you want to store the file in.",
                },
                "content": {
                    "type": "object",
                    "description": "The content you want to save to file.",
                },
                "description": {
                    "type": "str",
                    "description": "A description of the file and its purpose.",
                },
            },
            "required": ["file_name", "filepath", "content"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the file.",
                },
                "filepath": {
                    "type": "string",
                    "description": "The path to the directory you'd like to save the file in. If left blank, the file is saved in the root directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The content you want to save to file.",
                },
            },
            "required": ["file_name", "content"],
        },
    },
]

communication = [
    {
        "name": "send_imessage",
        "description": "Send an iMessage on the user's behalf.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The path to the directory the file is located.",
                },
                "filepath": {
                    "type": "string",
                    "description": "The full path to the file",
                },
            },
            "required": ["filepath"],
        },
    },
]


def send_imessage(email, message):
    applescript = f"""
    set theEmail to "{email}"
    set theMessage to "{message}"
    tell application "Messages" to send theMessage to participant theEmail of (account 1 whose service type is iMessage)
    """

    subprocess.run(["osascript", "-e", applescript])


send_imessage("new.email@example.com", "Your new message goes here.")
