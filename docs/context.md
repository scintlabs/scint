# Context

## Files

Scint provides language models with access to three contextual representations of directories it has access to:

- High-level context: A directory map with file names, metadata, and attributes as well as structure of the directory, providing a contextual overview
- Balanced context: descriptions and file metadata of each file within a directory map
- Focused context: the full file, or a fixed-size chunk with contextual links to the other chunks for full, effective context

Generally speaking, indexes files into chunks of roughly 1024 characters. While small limited to stated context windows of frontier models, detailed tasks often require more of a model's "attention," and stuffed context windows can lead to less favorable task results. Smaller chunks allows the model to focus on a task and allows for enough of its window to pass in system prompts, a directory map, and maintain a conversation with the user.

## Code

Code parsing is more granular. Scint uses tree-sitter to parse and contextualize source files. This provides another abstract representation similar to a directory mapping, but at the individual file level. These file maps provide:

- Definitions of each block within source files, e.g., imports, classes, functions, variables
- Instrinsic and extrinsic code details, including arguments, return values as well as dependencies, code paths, and so on
- Referencable and editable on a per-block basis and indexed for hybrid search

For code editing tasks, Scint can focus a single file along with intra-file code blocks relevant to this file. Alternatively, it can reference code maps, modifying or rewrite at the block level. This architecture and lifecycle ensures efficient handling of messages, data, and files, leveraging contextual information to provide relevant responses and maintain system performance.

