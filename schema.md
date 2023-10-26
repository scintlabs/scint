CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE request_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE keyword_categories (
    keyword_id SERIAL PRIMARY KEY,
    keyword_name VARCHAR(255) NOT NULL,
    parent_id INT REFERENCES keyword_categories(keyword_id),
    UNIQUE(keyword_name, parent_id)
);

CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    request_category_id INT REFERENCES request_categories(category_id),
    message_content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE message_keywords (
    message_id INT REFERENCES messages(message_id),
    keyword_id INT REFERENCES keyword_categories(keyword_id),
    PRIMARY KEY (message_id, keyword_id)
);

CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    description TEXT NOT NULL,
    due_date TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE documents (
    doc_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    content JSONB NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE EXTENSION cube;
