import asyncio
from core.observer import Observer
from core.state import State
from core.cli import run_cli

if __name__ == "__main__":
    asyncio.run(run_cli())
