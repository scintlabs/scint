from typing import Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from services.logger import log

# curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"role": "user", "content": "test message", "name": "ScintDiscord"}'
