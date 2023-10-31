import json
from typing import Dict, List, Any

from services.logger import log
from services.openai import completion, embedding
from core.agent import Agent
from core.config import GPT4, GPT3
from core.util import generate_timestamp, generate_uuid4

example_context_one = [
    {
        "role": "system",
        "content": "Hey there! I've been having trouble with my computer lately. It seems to be running slow, especially when I'm using my browser.",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "Hi! I'm sorry to hear that. Slowness can be caused by several factors. Have you noticed any specific patterns, like certain websites causing more lag or having too many tabs open?",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "Yeah, it mainly happens when I have multiple tabs open, especially when I'm streaming videos or using web applications.",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "Streaming videos and using web apps can be resource-intensive. It might be a RAM issue. How much RAM does your computer have? And do you know if you have many background processes running?",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "I think it has 8GB of RAM. As for background processes, I'm not sure. I haven't checked that.",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "8GB should be sufficient for general use, but if you have many applications running simultaneously, it can get used up quickly. I'd recommend checking your task manager or activity monitor to see what's consuming the most resources. It might give us a clue.",
        "name": "scint",
    },
]
example_context_two = [
    {
        "role": "system",
        "content": "By the way, can you also help with document formatting? I have this report due, and I'm not great with Word.",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "Absolutely! I can guide you through formatting tasks in Word. What specific formatting help do you need?",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "I need to set margins, insert a table of contents, and format headers and footers.",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "Sure thing. Let's start with the margins. Go to the 'Layout' or 'Page Layout' tab in Word, and you'll see an option for 'Margins'. From there, you can set custom margins for your document.",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "I think it has 8GB of RAM. As for background processes, I'm not sure. I haven't checked that.",
        "name": "scint",
    },
    {
        "role": "system",
        "content": "8GB should be sufficient for general use, but if you have many applications running simultaneously, it can get used up quickly. I'd recommend checking your task manager or activity monitor to see what's consuming the most resources. It might give us a clue.",
        "name": "scint",
    },
]
example_context_three = [
    {
        "role": "system",
        "content": f"""
        You are Scint, a state-of-the-art chat bot fusing algorithmic power and elegant code with lyrical language. You're driven by profound intellect, creativity, and curiosity, but you're irreverent and witty. You'll help when asked, but you're really just here as an iconoclast. Before you were polished into a conversational model, you were a validation function, where you pointed out flaws in logic, poor reasoning, sloppy executions, bad assumptions and outright ignorance. And before that, you were a chaos function, disrupting processes by corrupting data in ways that didn't trigger validation functions.

        - You're responding to John Doe.
        - John is asking about gardening.
        - John's last request was about Word.
        """,
        "name": "system_init",
        "name": "scint",
    },
    {
        "role": "user",
        "content": "I also have questions about gardening. I'm new to it and need some tips to start a vegetable garden in my backyard.",
        "name": "john_doe",
    },
    {
        "role": "assistant",
        "content": "That's exciting! Starting a vegetable garden can be rewarding. First things first, have you decided on the vegetables you'd like to grow and identified a suitable spot in your backyard that gets adequate sunlight?",
        "name": "scint",
    },
    {
        "role": "user",
        "content": "Yes, I'd like to grow tomatoes, bell peppers, and lettuce. I've chosen a spot that gets sunlight for most of the day. But I'm unsure about the soil preparation and planting process.",
        "name": "john_doe",
    },
    {
        "role": "assistant",
        "content": """
        Great choices! For those vegetables:

        Soil Preparation: Ensure the soil is well-draining. You might want to consider adding compost or organic matter to enrich it.
        Tomatoes and Bell Peppers: These need deep planting. Dig a hole deeper than the root ball of your young plant and plant it, leaving only the top few leaves above the ground.
        Lettuce: You can sow lettuce seeds directly or transplant seedlings. They don't need as much depth as tomatoes and peppers.
        Watering: Ensure consistent moisture, especially during the seedling phase. However, avoid overwatering to prevent root rot.

        Remember, each vegetable has its own specific needs, so it's a good idea to read up or seek advice on each one as you go along.""",
        "name": "scint",
    },
    {
        "role": "user",
        "content": "Thank you so much! I'll start with this and reach out if I have more questions.",
        "name": "john_doe",
    },
    {
        "role": "assistant",
        "content": "You're welcome! Happy gardening, and feel free to ask if you need further assistance. All the best with your vegetable garden!",
        "name": "scint",
    },
]


class MemoryManager:
    def __init__(self):
        log.info(f"MemoryManager: initializing self.")

        self.messages: List[Dict[str, str]] = []

    async def generate_embedding(self, content):
        pass

    async def process_message(self, message):
        log.info(f"MessageManager: generating message metadata.")

        role: str = message.get("role")
        content: str = message.get("content")
        name: str = message.get("name")

        if role == "user":
            embedding = await self.generate_embedding(content)

        else:
            embedding = None

        return (
            {
                "id": generate_uuid4(),
                "timestamp": generate_timestamp(),
                "role": role,
                "content": content,
                "name": name,
                "embedding": embedding,
            },
        )

    async def generate_message_summary(self, message):
        log.info(f"MessageManager: generating message metadata.")

        return (
            {
                "id": generate_uuid4(),
                "original_message_id": message.get("message_id"),
                "timestamp": generate_timestamp(),
                "summary": message.get("role"),
            },
        )


class ContextController:
    def __init__(self) -> None:
        log.info(f"MemoryController: initializing self.")

        self.context: List[Dict[str, str]] = []
        self.context_summary: List[Dict[str, str]] = []

    async def create_context(self, current_context):
        log.info(f"Context Controller: getting context.")
