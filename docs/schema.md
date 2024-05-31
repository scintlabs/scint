# Schema

## Concrete

Root
└── Structure
    └── Container
        └── Model

Controller
├── Aspect
│   ├── Prompts
│   │   ├── Identity
│   │   ├── Instruction
│   │   ├── Modifier
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

Controller
├── Threads
│   └── Thread
│       ├── Messages
│       ├── Files
│       ├── Links
│       ├── Events
│       └── UserManager
├── Composer
│   └── Context
│       ├── Prompts
│       └── Functions
└── Context
    ├── Prompts
    ├── Functions
    ├── Thread
    ├── People
    ├── Prompts
    └──