# Data

## StructType (Structures)

Structs serve as the outer enclosures or nodes, the "skeleton" of Scint's data architecture:

- Acts as composite nodes that can contain other StructType or ContainerType objects.
- Each StructType can have its unique identifiers, metadata, and methods that govern its interaction with other structures and containers.
- Can include methods for dynamic interaction with its contents, such as adding or removing structures, searching, and navigating through linked structures.
- Flexibility: Allow StructType objects to dynamically define their relationship with contained objects, either as direct children, linked through references, or even connected via more complex graph-based relationships.

## ContainerType (Containers)

ContainerType, on the other hand, are strictly for data handling. These are the "leaves" or "content holders" in Scint's data:

- Designed to hold and manage data elements (like messages, files, functions, etc.). Containers should be used to encapsulate the actual content within the structures.
- Should provide efficient access and manipulation methods for the data they hold, such as append, insert, delete, iterate, and others.
- Containers might also manage metadata specific to the data they hold but should not manage or manipulate other ContainerType or StructType directly.
- Interactions: Primarily interacts with the data within, offering methods to process or respond to changes in data state (like refreshing data, clearing content, etc.).


# Data

- Create and initialize base projects
    - Project metadata
    - Project map
    - Directory metadata
    - Individual file metadata

- Start new project
- Create root folder
- Select project type, frameworks, package manager, etc.
- Model calls functions to create directory map
- Run the directory map function

Controller
├── Context
│   ├── Promptss
│   │   ├── Identity
│   │   ├── Instructions
│   │   ├── Modifiers
│   │   └── Target
│   └── Functions
│       ├── Core
│       ├── Build
│       └── Traverse
├── Thread
│   ├── Messages
│   │   ├── UserMessage
│   │   └── AssistantMessage
│   ├── Schedule
│   │   └── Event
│   ├── Files
│   │   ├── Code
│   │   ├── Note
│   │   └── Image
│   └── Links
│       └── Link
└── Composer
    └── Context
        ├── Aspect
        └── Thread
        """
        ### Summary of `schema/messages.py`

        #### Purpose
        `messages.py` defines the structure of messages within the application, catering to various types of content and incorporating advanced features like dynamic content rendering based on the message type.

        #### Functionality
        - **Message Classification and Content Handling**: Provides structures for handling message classifications, content transformations, and rendering based on content type.
        - **Dynamic Message Creation**: Messages are dynamically created based on content type, with special handling for embedded code blocks or plain text.

        #### Interaction with Other Modules
        - Likely interacts with messaging and content processing modules, utilizing dynamic content rendering for user interfaces or logs.
        """
