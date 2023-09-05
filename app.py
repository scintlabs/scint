import asyncio

from fastapi import FastAPI, WebSocket, HTTPException, Depends, Body

from base.definitions.types import Message
from base.chat import send_message
from base.cli import run_cli
from util.logging import logger


asyncio.run(run_cli())
