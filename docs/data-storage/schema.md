## Postgres Schema

``` sql
-- Messages Table
CREATE TABLE messages (
    message_id UUID PRIMARY KEY,
    role TEXT NOT NULL CHECK (role IN ('system', 'user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    response_id TEXT
);

-- Keywords Table
CREATE TABLE semantic_tags (
    tag_id UUID PRIMARY KEY,
    tag TEXT NOT NULL,
    message_id UUID REFERENCES messages(message_id)
);

-- Functions Table
CREATE TABLE functions (
    function_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    parameters JSONB
);

-- Function Calls Table
CREATE TABLE function_calls (
    call_id UUID PRIMARY KEY,
    function_id UUID REFERENCES functions(function_id),
    response_id TEXT
);

-- Conversations Table
CREATE TABLE conversations (
    conversation_id UUID PRIMARY KEY,
    start_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    end_timestamp TIMESTAMP
);

CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL, -- consider hashing the password
    email TEXT NOT NULL UNIQUE,
    date_created TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE projects (
    project_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    name TEXT NOT NULL,
    description TEXT,
    date_created TIMESTAMP NOT NULL DEFAULT NOW(),
    deadline TIMESTAMP
);

CREATE TABLE tasks (
    task_id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(project_id),
    user_id UUID REFERENCES users(user_id),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    date_created TIMESTAMP NOT NULL DEFAULT NOW(),
    deadline TIMESTAMP
);

CREATE TABLE notes (
    note_id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(project_id),
    task_id UUID REFERENCES tasks(task_id),
    user_id UUID REFERENCES users(user_id),
    content TEXT NOT NULL,
    date_created TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE documents (
    document_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    data JSONB,
    date_created TIMESTAMP NOT NULL DEFAULT NOW()
);
```



