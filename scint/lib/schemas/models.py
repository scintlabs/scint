from __future__ import annotations

from typing import Dict, Any
from datetime import datetime as dt
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str = Field(default_factory=lambda: str(uuid4()))
    created: str = Field(default_factory=lambda: dt.now().isoformat())
    modified: str = Field(default_factory=lambda: dt.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)
    model_config = ConfigDict(arbitrary_types_allowed=True)
