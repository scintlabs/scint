# Lifecycles

## Threads and Messages

### Orphan Threads

- Linked List
- Marked inactive after 86400 without updates
- Marked stale after 86400 without updates
- Queued for pruning after 86400

### Standard Threads

- Linked List
- Attached to memory tree
- Queued for semantic and keyword indexing
- Marked inactive after 259200
- Marked stale after 259200
- Queued for collapse after 259200

### Thread Processing

Psuedo code for message processing by ThreadManager in core modules:

```
message received
    semantic search memory with message.content
        if message.content matches existing thread in memory tree
            attach to thread
            return activated thread
        create new orphan
```

```
collapse thread
    create new thread at message parent
    create list of all relationship links in thread
    attach links to new thread
    concatenate message into single message
    send message to ai for summarization
    append result to new thread
    prune old thread
```

```
prune thread
    delete thread
    if thread.parent
        add deletion event to log with pointer to collapsed thread
    add deletion event to log
```

## Files and Data

The data lifecycle encompasses two categories of data: internal and contextual. Internal data refers to data passed via configuration, including documents, notes, links to online data, and so on. Contextual data refers to anything loaded ad-hoc during regular interactions.