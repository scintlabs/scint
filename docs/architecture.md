# Architecture

Scint
├── Server Init
│   ├── Core Server
│   ├── Event Log
│   ├── Settings Manager
│   │   ├── System Settings
│   │   │   ├── Storage
│   │   │   ├── Search
│   │   │   └── Message Broker
│   │   └── User Settings
│   │       ├── Permissions
│   │       ├── Paths
│   │       └── Integrations
│   ├── System Modules
│   │   ├── Storage Controller
│   │   │   ├── Prompts
│   │   │   ├── Functions
│   │   │   ├── Files
│   │   │   ├── Threads
│   │   │   └── Search Indexes
│   │   ├── Search Controller
│   │   │   ├── Files Index
│   │   │   └── Threads Index
│   │   └─ Services
│   │      ├── Message Broker
│   │      └── Intelligence Provider
│   ├── Core Modules
│   │   ├── Context Controller
│   │   │   ├── Composer
│   │   │   └── Context Pool
│   │   ├── Process Controller
│   │   │   ├── Builder
│   │   │   └── Process Pool
│   │   ├── File Manager
│   │   ├── Thread Manager
│   │   └── Loader Library
│   │       ├── Directory Mapper
│   │       ├── File Parser
│   │       ├── Code Parser
│   │       └── Loader
│   └── Integrations
│       └── Not Implemented
└── Ready