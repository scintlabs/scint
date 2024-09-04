# Scint

> “Finally there he returns, trying to imitate in his walk the inflexible stiffness of some kind of automaton while carrying his tray with the recklessness of a tight-rope-walker by putting it in a perpetually unstable, perpetually broken equilibrium which he perpetually reestablishes by a light movement of the arm and hand. All his behavior seems to us a game. He applies himself to chaining his movements as if they were mechanisms, the one regulating the other; his gestures and even his voice seem to be mechanisms; he gives himself the quickness and pitiless rapidity of things. He is playing, he is amusing himself. But what is he playing? We need not watch long before we can explain it: he is playing at being a waiter in a café."

— Jean-Paul Sartre, *Being and Nothingness*

## Overview

A flexible, extensible system that allows LLMs to interact with and manipulate abstract resources and data at a high level. Provides clear, consistent interfaces that LLMs understand and use effectively.

Context > Thread > Process > Task

- Context represents the system state at any given moment
- Threads are scoped collections of processes, data, or conversations
- Processes are scoped collections of tasks with focused, sliding contexts

## Architecture

- **Hierarchical Language Model Processes**: Create a hierarchy of LLM processes, each responsible for different levels of abstraction or entire domains. Higher-level LLMs can decompose complex tasks into simpler subtasks for lower-level LLMs.
- **Context-based Framework**: Create specific context objects for different types of actions or resources. Define a set of high-level operations for each context that LLMs can invoke. Implement these operations as methods within each context class.
- **Event-driven Architecture**: Utilize the existing message processing structure to create a communication layer between LLMs and the system. Define a standardized message format that includes the context, action, and parameters.

### Context as Identity

- **Dynamic Context Creation**: Allow LLMs to create new contexts or modify existing ones using the create_context function. This enables the system to adapt and expand its capabilities based on LLM inputs.
- **Resource Abstraction**: Use the Container context to represent abstract resources that LLMs can manipulate. Implement methods within the Container class to perform high-level operations on these resources.
- **Task Orchestration**: Utilize the Composer context to create complex workflows or sequences of actions across different contexts. Allow LLMs to define and execute these workflows.
- **Asynchronous Processing**: Leverage the existing asynchronous structure to handle multiple LLM requests concurrently. Use the Thread context to manage and coordinate parallel processing of tasks.
- **State Management**: Implement a state management system using the ContextMap and ContextMapView classes. Allow LLMs to query and modify the state of different contexts.
- **Error Handling and Logging**: Utilize the existing logging mechanism (__logger__ decorator) to provide feedback to LLMs about the execution of their requests. Implement error handling mechanisms that can provide meaningful feedback to LLMs.
- **Natural Language Interface**: Create a natural language processing layer that can interpret LLM requests and map them to specific context actions. This could involve using the LLM itself to parse and understand more complex instructions.
