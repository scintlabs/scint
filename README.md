# Scint

> ⚠️ **Attention**
>
> Scint is a work in progress. Code, APIs, and documentation are subject to change without notice.

Scint is an experimental Python framework for building goal-directed, AI-driven systems. With a modular design and an emphasis on extensibility, Scint aims to provide a foundation for building complex, context-aware agents capable of reasoning, memory management, and structured interaction—both with users and external resources.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture and Concepts](#architecture-and-concepts)
    - [Core](#core)
    - [Composition](#composition)
    - [Processes](#processes)
    - [Memory](#memory)
3. [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)

---

## Overview

Scint provides a high-level, flexible platform for integrating LLMs into Python applications. It abstracts away much of the complexity involved in:

- Handling prompt/response pipelines.
- Maintaining conversational or contextual memory.
- Exposing Python functions in a manner that LLMs can understand and reliably call.
- Managing workflows (processes) and orchestrating multi-step tasks.

**Why Scint?**

- **Structured AI Interactions**
   Scint aims to bridge structured application logic with the unstructured world of LLM responses, ensuring more consistent and predictable outputs.

- **Extendability**
   From adding new aspects (logging, indexing, embeddings) to hooking up different LLM backends, Scint is built to grow with your needs.

- **Experimental Playground**
   While not yet production-ready, Scint offers a glimpse of how advanced applications might guide, critique, and orchestrate AI reasoning in complex domains.

## Architecture and Concepts

- **Process Orchestration**
   - **Orchestrator** coordinates multi-step tasks and can chain processes (like searching a database, parsing data, generating text, etc.) under a single flow.
   - **Controller** acts as a higher-level manager or gateway for these processes.

- **Context and Memory Management**
   - **Memory** abstractions (e.g., `Context`, `Threads`, `Thread`) organize conversation data, embeddings, events, and files.
   - **Composer** automatically selects and augments contextual data based on similarity, ensuring relevant information is recalled at each step.

### Core

**Controller**

### Composition

One of the core design principals of Scin is its dynamic compositionality, realized through two core abstractions: Aspects and Structs. This design is geared toward enabling language models (and other higher-level frameworks) to self-compose new types and behaviors at runtime by instantiating and combining these building blocks—an approach reminiscent of Rust’s structs and traits, albeit achieved here via Python’s dynamic metaclass machinery.

**Aspects**

Aspects are analogous to “protocols” or “traits” that define contracts for functionality. They use a custom metaclass, AspectType, to track which attributes (data) and methods (behaviors) a class must implement. Any class marked as an Aspect (or subclass thereof) effectively declares, “I provide certain methods or data; anything using me needs to satisfy these protocols.”

1.	Protocol Checking

AspectType enforces a mini “protocol” system: if a class (or instance) claims to implement a particular Aspect, it must define all required attributes and methods in its namespace. If they’re missing, a TypeError is raised. This ensures consistency at runtime—even if classes are generated on-the-fly (e.g., by a language model).

2.	Decorator Injection

Each Aspect may optionally declare a decorator method, which is applied to all public methods in its subclasses. This allows for cross-cutting behaviors—like logging, instrumentation, or AI-driven transformations—without altering the base logic of the method. It’s a powerful way to inject functionality into your classes dynamically.

3.	Dynamic Composition

Because Aspects are metaclass-driven, you can compose multiple Aspects into a single class. Suppose you have `LoggingAspect` and `SecurityAspect`: you can create a new class that incorporates both, and AspectType ensures everything lines up. This means you can quickly spin up new objects with multiple cross-cutting features attached—particularly useful if you’re generating code from a language model that decides what “traits” a class needs on the fly.

**Structs**

Where Aspects handle contracts for behavior, Structs provide a highly flexible, dataclass-like container for your data hierarchy. The StructType metaclass collects annotations from all base classes, auto-generates fields, then transforms the resulting class into a Python dataclass.

1.	Data Composition

Struct are designed for strongly typed, hierarchical data. A Struct can contain other nested Structs, as well as lists or sets of them. This recursive composition is essential for building up complex data models—again, driven dynamically if needed.

2.	Validation and Inheritance

StructType ensures that subclasses include at least the fields required by their parent. This is enforced through __subclasscheck__. Meanwhile, the __post_init__ method auto-initializes any default factories, giving you a predictable state for each new instance.

3.	Hierarchical Organization

Common utility methods (add_child, remove_child, walk) reflect how Structs often model tree-like relationships, enabling you to build complex, nested data structures that can be easily traversed, inspected, and modified.

4.	AI-Friendliness

The model and from_dict methods illustrate how these structures can be serialized and deserialized, making them convenient for AI-based generation and consumption. A language model can dynamically craft JSON or dictionary data that can be turned into a Struct—or multiple nested Structs—at runtime. This empowers a model to “self-compose” new data structures on the fly, furthering the dynamic spirit of the system.

### Processes

**Orchestrator**

### Memory

**Composer**

### Structures

**Mapper**

## Getting Started

### Installation

### Usage

## Contributing
