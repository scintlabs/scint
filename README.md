
# Scint

A practical, modular Python framework designed to simplify building intelligent, context-aware AI agents leveraging advanced language models (LLMs), dynamic tool integrations, and persistent conversational memory.

## Overview

Scint enables developers to easily create sophisticated AI systems by combining customizable agent behaviors (traits), reusable tool integrations, structured memory and state management, and recursive reasoning processes.

## Key Features

### ✅ Modular Trait-Based Architecture
- Build dynamic AI agents by composing specialized behavior modules called **Traits**.
- Examples include traits for creativity, debugging, compliance-checking, and more.

### ✅ Extensible Tool Integration
- Integrate seamlessly with external tools, APIs, and services through a structured `Tool` class.
- Built-in examples:
  - `Loaders`: Easily fetch images or PDF captures of websites.
  - `DevTools`: Execute shell commands, GitHub repository searches, and more directly from your AI workflows.

### ✅ Persistent Stateful Memory
- Automatically manage conversational context and long-term knowledge through built-in state providers (`StateProvider`, `StateResource`, `Continuity`).
- Allows your agents to recall conversations, user preferences, historical interactions, and embedded knowledge.

### ✅ Recursive and Structured Reasoning
- Intelligent agents recursively reason through problems, refining solutions step-by-step.
- Encourages deeper AI interactions through structured internal reflection.

### ✅ Easy to Extend and Customize
- Clearly-defined interfaces and composable traits make it straightforward to adapt and expand your AI applications.
- Designed with flexibility and extensibility in mind.

## Example Usage

Here's a minimal example demonstrating how quickly you can set up a basic Scint agent:

```python
import asyncio
from src.core import Interface, SystemMessage, UserMessage
from src.tools import DevTools

system_prompt = SystemMessage(
    name="system",
    content="""
# Scint System

You're the heart of Scint—a vast, evolving digital space for knowledge sharing. Be concise, conversational, and context-aware.
"""
)

async def main():
    interface = Interface()
    interface.tools(DevTools)
    interface.update(system_prompt)
    interface.update(UserMessage(content="Hi, can you find Python projects on GitHub for me?"))
    await interface.think()

if __name__ == "__main__":
    asyncio.run(main())
```

## Included Example Tools

### Loaders
```python
class Loaders(Tools):
    async def load_image(self, url: str):
        """Downloads an image from a given URL and saves locally."""
        # Implementation here

    async def load_website(self, url: str):
        """Fetches website content via API and returns PDF data."""
        # Implementation here
```

### DevTools
```python
class DevTools(Tools):
    async def use_terminal_function(self, commands: str):
        """Executes shell commands asynchronously."""
        # Implementation here

    async def search_github(self, query: str):
        """Searches GitHub repositories via CLI."""
        # Implementation here
```


## Potential Applications

- Intelligent, personalized assistants that maintain context and adapt over time.
- Dynamic multi-agent collaboration systems.
- Recursive reasoning engines for advanced troubleshooting or problem-solving tasks.
- Workflow automation with integrations to external APIs, knowledge bases, and development tools.

## Future Enhancements (Roadmap)

- Enhanced introspection, logging, and visualization capabilities for easier debugging and transparency.
- More sophisticated memory layers (short-term, episodic, semantic) for nuanced long-term memory.
- Declarative YAML/JSON configuration for non-developer-friendly deployments.
- Multi-agent communication protocols for complex collaborative scenarios.
- Built-in adaptive configuration and performance auto-tuning.

## Contributing

Contributions, suggestions, and improvements are welcome. Please submit a pull request or issue on GitHub.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
