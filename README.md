# Scint

> ⚠️ **Attention**

> Scint is experimental and very much a work in progress. Presently, this README functions as a scattering of ideas and notes, much of which was authored by language models. While the documentation reflects ideas represented in the accompanying code, very little in either the former or latter is set in stone. In other words, everything in this repo is subject to chaotic change, so tread lightly.

Scint is a Python framework designed to build intelligent, goal-directed systems that interact seamlessly with large language models (LLMs). It provides a structured approach to create AI agents capable of complex behaviors, context management, and interaction with various resources and data at a high level of abstraction. Scint emphasizes flexibility and extensibility, allowing developers to define clear and consistent interfaces that LLMs can understand and utilize effectively.

## Setup

```bash
 poetry run python3 src/app.py
 ```

## Features

- Modular Architecture: Scint is built with a modular design, making it easy to extend and customize components according to specific needs
- Asynchronous Processing: Leverages Python’s asyncio library for handling multiple tasks concurrently, enabling efficient processing of numerous interactions
- State Management: Implements a robust state management system using contexts and chain maps, allowing for dynamic context creation and manipulation
- Event-Driven Communication: Utilizes an event-driven architecture to handle communication between different parts of the system, including message passing and function invocation
- Integration with LLMs: Provides structures for composing prompts, handling LLM responses, and managing interactions, making it suitable for applications involving AI language models
- Resource Abstraction: Offers abstract representations of resources (like files, messages, and functions) that can be manipulated programmatically
- Persistence and Search: Includes components for data persistence using databases like PostgreSQL and search capabilities using tools like Meilisearch

## Architecture

Scint’s architecture is composed of several key components that work together to create a flexible and extensible framework:

### Context and State Management

- Context Objects: Scint uses context objects to encapsulate the state and behavior of different parts of the system. Contexts can be nested and are designed to be dynamically created and modified.
- State Handling: The framework employs chain maps and custom state classes to manage state across different contexts, enabling shared and isolated states as needed.

### Components and Entitys

- Components: At the core, Scint defines components that encapsulate functionality. Components can be simple functions or more complex classes that represent parts of the system.
- Entitys: Entitys are higher-level constructs that organize components into workflows or processes. They allow for complex behaviors to be defined by combining simpler components.

### Messaging and Events

- Message Models: Scint defines models for different types of messages (input, output, system) using Pydantic for data validation and serialization.
- Event Handling: The framework includes an event system that captures method calls, results, and other significant occurrences within the system, facilitating debugging and introspection.

### Asynchronous Processing

- Async Functions: Many components and functions in Scint are designed to be asynchronous, enabling the system to handle multiple tasks without blocking.
- Concurrency: By utilizing asyncio, Scint can manage concurrent interactions, which is crucial for applications that require handling multiple user sessions or background tasks.

### Integration with External Processs

- WebSocket Support: Scint includes support for WebSocket connections, allowing real-time communication with clients.
- Database Interaction: Provides classes for interacting with databases like PostgreSQL for data persistence.
- Search Functionality: Integrates with search services such as MeiliSearch to offer advanced search capabilities within the system.
- Third-Party APIs: Includes components for interacting with external APIs, such as GitHub repositories or web content fetching.

### LLM Interaction

- Prompt Management: Defines structures for creating and managing prompts sent to LLMs, including system prompts, user messages, and assistant responses.
- Function Execution: Supports the execution of functions based on LLM outputs, allowing the system to perform actions as directed by the AI’s responses.
- Embedding and Similarity: Implements methods for generating embeddings and calculating similarity scores, which can be used for tasks like intent recognition or content matching.
