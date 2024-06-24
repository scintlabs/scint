# State and Context

| Abstract   | Focused        | Streaming |
| ---------- | -------------- | --------- |
| Mapping    |                |           |
| ⮮⮭         |                |           |
| Parsing -> | Working        |           |
|            | ⮮⮭             |           |
|            | Interaction -> | Execution |
|            |                |           |

Abstract, focused, and streaming represent the available states of a single node within the primary data structure. Meanwhile, Mapping, Parsing, Working, Interacting, and Executing represent concurrent, asynchronous context objects, which the nodes host as visitors. Functionality is determined by:

The context category
The state of the node
Functions and instructions assigned on every interaction based on context, state, and user feedback; both of these components are retrieved via hybrid keyword and vector search

In other words, state notwithstanding, each context type has dozens of functions and capabilities at its disposal, selected and equipped based on real-time analysis of the user's input and the state of the entire system.

### Abstract

Abstract, the default state, provides access to edge relationships to other nodes, data labels for semantic understanding of the system's corpus of knowledge, and contextual metadata relevant to any data the node has access to, tuned for breadth-first search and traversal. This state maintains immutable references to its data, such as keywords, embeddings, abstract syntax trees, etc., but cannot access the actual data.

Mapping contexts utilize the abstract state, and this context and state define new data structures and relationships within the system. Parsing contexts parse data references to load concrete data, transitioning a node into the focused state.

### Focused

When a node enters a Focused state, it converts its immutable data references into mutable data, which it loads either from the filesystem or the document database. Actions taken in this state are primarily user-guided via a chat interface, where the user provides instructions and feedback, and the system modifies the node's data in place.

A focused node maintains direct edge connections with the surrounding abstract node data references, which provides the context with highly-relevant information without overloading the limited context window.
Lastly, a user can request workflow execution, which transitions a node into streaming mode.

### Streaming

Define workflows using edges/relationships between nodes as well as within the nodes themselves. Each edge can have properties that define the workflow steps, conditions, parameters, as well as any flow-specific logic, like loops, conditionals, and so on. Meanwhile, focus nodes (nodes within the workflow) supply concrete data, and the abstract nodes connected to those nodes provide contextual augmentation.

Streaming nodes essentially copy data from the focused state, create a new instance using predefined and dynamic workflows, and assign the new data to the destination node or nodes. They do not store data themselves—they only contain workflow logic.
Additional considerations:

- Create a single "overview" context, separate from the context being passed from node to node, to maintain a high-level understanding of the system's state and goals.
- Develop a "look-ahead" mechanism on node pathways to allow reasoned traversal using LLM calls, enabling the system to anticipate and optimize its actions.
- Implement message passing to nodes within the path of execution, pre-building context and/or informing traversal decisions to improve efficiency and accuracy.
- Ensure that the system can handle various data types, such as structured data (e.g., databases), unstructured data (e.g., text documents), and semi-structured data (e.g., JSON, XML).
- Incorporate a caching mechanism to store frequently accessed data and reduce latency during node traversal and data retrieval.
Implement a robust error handling and recovery system to maintain system stability and data integrity in case of failures or unexpected events.
