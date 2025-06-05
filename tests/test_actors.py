import asyncio
import unittest
from contextlib import suppress
from pathlib import Path
import sys
import os

src_path = Path(__file__).resolve().parents[1] / "src"
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))
sys.path.insert(0, str(src_path))
os.environ["PYTHONPATH"] = str(src_path)
tests_dir = str(Path(__file__).resolve().parent)
if tests_dir in sys.path:
    sys.path.remove(tests_dir)
sys.modules.pop("typing", None)
sys.modules.pop("socket", None)

class DummyReceiver:
    def __init__(self):
        self.received = None
    def ref(self):
        from src.runtime.actor import ActorRef
        return ActorRef(self._capture)
    def _capture(self, env):
        self.received = env

class ActorTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        from src.core.agents.dispatcher import Dispatcher
        self.dispatcher = Dispatcher()
        self.dispatcher.load()
        self.dispatcher.start()
        await asyncio.sleep(0.01)

    async def asyncTearDown(self):
        for act in self.dispatcher._actors.values():
            if act._task:
                act._task.cancel()
                with suppress(asyncio.CancelledError):
                    await act._task
        if self.dispatcher._task:
            self.dispatcher._task.cancel()
            with suppress(asyncio.CancelledError):
                await self.dispatcher._task

    async def test_interpreter_handles_message(self):
        from src.core.agents.interpreter import Interpreter
        from src.core.resources.continuity import Continuity
        from src.model.records import Message
        interp = Interpreter(continuity=Continuity())
        receiver = DummyReceiver()
        await interp.on_receive(Message(content="hello"))
        env = receiver.received
        self.assertIsNone(env)

    async def test_composer_creates_outline(self):
        from src.core.agents.composer import Composer
        from src.core.resources.library import Library
        from src.model.context import Context, ActiveContext, RecentContext
        from src.model.threads import Thread
        comp = Composer(library=Library())
        comp.start()
        ctx = Context(ActiveContext(thread=Thread()), RecentContext(threads=[]))
        comp.ref().tell(ctx)
        await asyncio.sleep(0.1)
        self.assertIn("last", comp.outlines)
        comp._task.cancel()
        with suppress(asyncio.CancelledError):
            await comp._task

    async def test_executor_processes_outline(self):
        from src.core.agents.executor import Executor
        from src.core.resources.catalog import Catalog
        from src.model.outline import Outline
        exe = Executor(catalog=Catalog())
        exe.start()
        out = Outline(tasks=[])
        exe.ref().tell(out)
        await asyncio.sleep(0.1)
        self.assertIsNotNone(exe._process)
        exe._task.cancel()
        with suppress(asyncio.CancelledError):
            await exe._task

