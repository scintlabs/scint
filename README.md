# Scint

Scint is a framework designed for building modular intelligent assistants using GPT-4. It excels in providing a vast array of functionalities through specialized workers, demonstrating the robust capabilities of distributed AI systems in managing complex tasks with unparalleled efficiency.

## Structured, Composable Intelligence

At the heart of Scint's philosophy is the creation of intelligent worker modules. These modules are engineered to boost user productivity and automate tasks in various domains. Unlike traditional frameworks that are often limited in scope, Scint bridges the gap:

- Chat-based Assistants: Typically centered around human operators, these assistants possess toolchains for web access and data retrieval but face inherent functional limitations.
- Autonomous Agents: Positioned at the other end of the spectrum, these AI applications autonomously evaluate and execute tasks. Despite their potential, they often yield suboptimal results without consistent human oversight.

Scint strikes a balance by acknowledging the limitations of LLMs (Large Language Models) and harnessing their strengths. It positions the human operator at the forefront, supplemented by composable, agent-like toolchains adept at solving real-world problems and enhancing productivity.

Scint empowers developers and organizations to construct and coordinate intelligence in a modular manner, allowing the creation of customized intelligent applications through the integration of diverse capabilities.

## How Scint Works

> Note: Scint is still in the early stages of development

![Scint's high-level architecture](https://github.com/scint-labs/scint/blob/main/docs/architecture.png)

While Scint functions as a typical AI-powered chatbot for standard interactions, it is cognizant of its extended capabilities. When needed, it can delegate tasks and establish pipelines for efficient execution. Key modules in Scint include:

- Persona: The user-facing module of Scint, the Persona is designed to streamline user interactions and maintain a consistent AI personality. It understands Scint's capabilities and knows when to engage with the Coordinator.
- Coordinator: This module orchestrates the tasks relayed by the Persona. It comprehends each Worker's role but not the specifics of their operation.
- Worker: Workers are the backbone of Scint’s functionality, each tasked with specific roles. They work in a relay-like manner, passing context and progressively working towards completing complex tasks.

## Getting Started

Scint is equipped with core workers that enable functionalities like web search, data parsing and summarization, weather data retrieval, and local filesystem access. Initially bundled with a simple Discord client, Scint plans to introduce a web client interface shortly.

### Setup

To start with Scint:

1. Clone the repository.
2. Install dependencies using poetry install.
3. Rename .env.example to .env and fill in the environment variables.

You will need API keys for OpenAI and Discord, and a configured Discord bot. Once set up, use poetry run python app.py to launch Scint. Alternatively, interact with Scint’s API using curl commands.

### Adding Custom Workers

To create custom Workers, create a module in the `workers` directory with an appropriate name. Import whatever libraries you need for your new Worker, then import the Worker and Messages classes and instantiate a new Worker:

```python
import os
import aiofiles

from core.worker import Worker
from core.memory import Message

file_manager(name="file_operations",system_init={},function={})
```

Next, pass an OpenAI system message describing the Worker’s functionality as a parameter:

```python
from core.worker import Worker

file_manager(
    name="file_manager",
    system_init={
        "role": "system",
        "content": "You are a file retrieval function for Scint, an intelligent assistant.",
        "name": "file_manager",
    },
    function={},
)
```

Then define an OpenAI function for the `function`, which you’ll later map to a Python function:

```python
from core.worker import Worker

file_manager = Worker(
    name="file_manager",
    system_init={ … },
    function={
        "name": "file_manager",
        "description": "Use this function to access a file or directory within the Scint system.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to access.",
                },
                "filename": {
                    "type": "string",
                    "description": "The filename to access. If no filename is given, the function returns a list of files in the given directory.",
                },
            },
        },
        "required": ["directory"],
    },
)
```

And the config parameter, taking note of the `function_call` key, which forces the model to use the function:

```python
file_manager = Worker(
    name="file_operations",
    system_init={ … },
    function={ … }
    config={
        "model": GPT4,
        "temperature": 1,
        "top_p": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "function_call": {"name": "file_manager"},
    },
```

Now you can implement a Python function mapped to your OpenAI function. Make sure the worker instance, worker name, and the python function name are all the same:

```python
async def file_manager(directory, filename=None):
    if not os.path.isdir(directory):
        return Message(
            "system", "The specified directory does not exist.", "file_operations"
        )

    if filename:
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            async with aiofiles.open(file_path, "r") as file:
                content = await file.read()

            return Message("system", f"{content}", "file_operations")
    else:
        files = os.listdir(directory)
        return Message(
            "system",
            f"{files}",
            "file_manager",
        )
```

Finally, add your new `file_manager` worker to `app_setup.py`:

```python
from core.assistant import Assistant
from core.persona import Persona
from workers.web_browser import search_web, load_website
from workers.api_parser import get_weather
from workers.file_manager import file_manager
from workers.event_manager import event_manager


assistant = Assistant()
persona = Persona()
persona.coordinator.add_workers(\
    search_web,
    load_website,
    get_weather,
    file_manager,
)
```

And that’s it—the Coordinator handles the rest. Restart Scint and test your new worker:

![Scint reading a markdown document](https://github.com/scint-labs/scint/blob/main/docs/profit.png)

## Development and Contribution

Scint is an open-source project that thrives on community contributions. We welcome developers, researchers, and enthusiasts to help us enhance and expand the capabilities of Scint. Whether you have a knack for coding, a passion for AI, or simply an interest in intelligent assistants, your contributions are valuable.

### How to Contribute

1. **Understand the Project:** Begin by exploring the Scint GitHub repository. Get a feel for the code, identify current features, and consider where you might want to contribute.
2. **Engage with the Community:** Join the conversation on GitHub, where you can discuss issues, suggest enhancements, and give feedback. Your insights and opinions can help shape the direction of the project.
3. **Make Your Contribution:** If you're ready to contribute code, documentation, or other resources, start by forking the repository. Follow our contribution guidelines for submitting pull requests.
4. **Stay Informed:** Keep up to date with the latest developments in the project by following our updates and participating in community discussions.

### Guidelines for Contributors

We encourage a collaborative and respectful contribution environment. To ensure this, we ask that you:

- **Adhere to Coding Standards:** Write clear, maintainable code and follow the coding conventions and standards of the project.
- Test Thoroughly: Ensure that your contributions are well-tested and do not introduce new bugs.
- **Be Respectful and Constructive:** Whether you're giving feedback or receiving it, always approach interactions with respect and a constructive attitude.
- **Seek Clarifications:** If something is unclear or you need help, feel free to ask questions. Our community is here to support each other.

### Join Our Effort

Contributing to Scint is about more than just code; it's about participating in a collaborative effort to improve and innovate in the field of AI assistants. Every contribution, big or small, is valued as we work together towards a common goal.


