# State Heirarchy

State -> Request -> Substate -> Subject -> State Object -> State

EventLoop
├── Listen
├── New Request -> Composition -> Eval
│
│       Compositions
│       ├── Search -> SearchSpace -> DataType
│       │   │
│       │   └── SearchSpaces and Types
│       │       ├── Internal (MapTypes)
│       │       │   ├── Procedures
│       │       │   │   ├── Instructions
│       │       │   │   └── Functions
│       │       │   └── Regions
│       │       │       ├── Locations
│       │       │       └── Waypoints
│       │       │           └── Containers
│       │       │               └── Collections
│       │       │                   └── Items
│       │       └── External (DataTypes)
│       │           ├── Filesystem
│       │           │   └── Directories
│       │           │       └── Files
│       │           └── Internet
│       │               ├── APIs
│       │               └── Websites
│       │
│       ├── Map -> Data -> MapType
│       └── Parse -> MapType -> Results
│           │
│           ├── ParseTypes
│           │   ├── Message
│           │   ├── Command
│           │   ├── Function
│           │   ├── Arguments
│           │   └── Procedure
│           │
│           └── ParseStrategies
│               ├── Reflect
│               └── InputLoop
│
├── Eval
└── New Response -> Listen

## Listen

1. Controller assigns request to context
2. Context transitions from listening to eval
3. Eval state inits composer

## Eval

1. Composer builds context
2. Composer uses current context's embedding and labels to search
3. Search returns prompts, functions to augment request
4. Request sent to language model for response generation
    1. Model generates arguments to call search, map, or parse functions
    2. Search, map, or parse function call transitions to inner eval state

## Inner Eval

1. If request for search
    - Go to Search state
2. If request for map
    - Go to Map state
3. If request for parse
    - Go to parse state

## Search State

1. Transition to search state
2. Eval search
3. If results are of DataType
    - Go to Map state with DataType

## Map State

1. Transition to Map state
2. Map data using appropriate strategy
3. If successful
    - Go to parse state with MapType

## Parse State

1. Transition to Parse state
2. Parse data using appropriate strategy
3. Generate response
    - Transition to Listen state
    - Return response


## Event Heirarchy

Event
├── User
│   └── Message
└── System
