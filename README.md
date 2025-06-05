# Scint

Scint is an experimental Python framework for building AI agents from small, composable pieces.  The code is structured around an asynchronous **actor** model.  Each actor receives messages via a mailbox and runs in its own `asyncio` task.

## Architecture

The entry point is the `Dispatcher` actor which instantiates three main workers:

* **Interpreter** – builds a conversational `Context` using the `Continuity` service.
* **Composer** – creates an `Outline` from that context using the `Library` of prompts and instructions.
* **Executor** – turns the outline into a `Process` and calls available tools from the `Catalog`.

```python
# src/core/agents/dispatcher.py
class Dispatcher(Actor):
    def load(self):
        idx = Indexes()
        self.spawn("interpreter", Interpreter, continuity=Continuity(indexes=idx))
        self.spawn("composer", Composer, library=Library(indexes=idx))
        self.spawn("executor", Executor, catalog=Catalog(indexes=idx))
```

Every actor inherits from `Actor` which manages a mailbox and a background task:

```python
# src/runtime/actor.py
@define
class Actor:
    _mailbox: Mailbox = Mailbox()
    _task: Optional[asyncio.Task] = field(init=False, default=None, repr=False)

    def start(self):
        if self._task is None:
            self._task = asyncio.create_task(self._runner())
```

### Continuity

`Continuity` tracks threads of conversation and performs semantic search over them. When a new `Message` arrives, the service assembles a `Context` object that blends the active thread, recent history and search hits:

```python
# src/core/resources/continuity.py
async def get_context(self, msg: Message):
    thread = await self.resolve_thread(msg)
    context = Context(
        active=ActiveContext(thread=thread),
        recent=RecentContext(threads=self.get_threads()),
        semantic=SemanticContext(embed=msg.metadata.embedding, search=self.search),
    )
    await context.update(msg)
    return context
```

### Library and Catalog

The `Library` loads instructions, outlines and tool specifications from the `config/` directory and stores them in a search index:

```python
# src/core/resources/library.py
async def _load_modules(self):
    await self._indexes.load_indexes()
    for cfg in ("directions", "outlines", "instructions", "tools"):
        with open(f"config/{cfg}.json", "r") as f:
            data = json.loads(f.read())
            setattr(self, cfg, data)
            if cfg == "tools":
                idx = await self._indexes.get_index("tools")
                records = [{"id": t.get("_sig"), **t.get("schema", {})} for t in data]
                await idx.update_documents(records)
```

`Catalog` collects callable tools from `src/core/tools` and registers their schemas for use during execution:

```python
# src/core/resources/catalog.py
async def _load_modules(self):
    module = import_module("src.lib.tools")
    for _, attr in inspect.getmembers(module):
        if inspect.isfunction(attr) and attr.__module__ == module.__name__:
            fp = generate_signature(attr)
            wrapper = tool(attr)
            self._tools.setdefault("functions", {})[fp] = wrapper.schema
            await self._register_wrappers(wrapper)
    await self._sync_index()
```

## Running

Running the package launches the bootstrap routine and a small FastAPI server:

```python
# src/__init__.py
async def main():
    await bootstrap()
    server = uvicorn.Server(
        uvicorn.Config(app=FastAPI(), host="127.0.0.1", port=8000, log_level="info")
    )
```

Invoke `python -m scint` to start the demo dispatcher and server.

## Repository Layout

- `src/core/agents/` – interpreter, composer and executor actors.
- `src/core/resources/` – services such as `Continuity`, `Library` and `Catalog`.
- `src/runtime/` – actor framework utilities.
- `config/` – JSON files describing prompts, outlines and tool metadata.
- `tests/` – unit tests.

## Contributing

Pull requests and issues are welcome.  The project is released under the MIT license.

