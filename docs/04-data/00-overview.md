# Data

## Models




Collection
├── Project
├── Book
├── Documents
├── Repo
└── Directory

Item
├── FileItem
├── CodeItem
├── Image
├── Instruction
├── Message
├── Function
└── Arguments

Instruction
Message
Function
Arguments


Scint
├── Core
│   ├── Context
│   │   └── Composer
│   │       ├── Context
│   │       │   ├── Instruction
│   │       │   ├── Function
│   │       │   └── Routine
│   │       └── Reference
│   │           ├── Map
│   │           └── snapshot
│   ├── ModelR
│   │   └── Region
│   │       ├── Waypoint
│   │       └── Location
│   │           └── Collection
│   │               ├── Collection
│   │               └── Item
│   │                   └── Data
│   └── Events
│       ├── Request
│       │   └── Message
│       │       ├── Instruction
│       │       └── Function
│       └── Response
│           ├── Message
│           └── Arguments
├── Dispatch
│   ├── Connections
│   ├── Queue
│   └── Router
├── Intelligence
│   ├── Providers
│   └── Parser
└── Services
    ├── Cache
    ├── Search
    └── Storage
