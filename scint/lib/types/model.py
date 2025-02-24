from __future__ import annotations

from typing import Any, Dict
from datetime import datetime as dt

from pydantic import BaseModel, ConfigDict, Field


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    created: str = Field(default_factory=lambda: dt.now().isoformat())
    modified: str = Field(default_factory=lambda: dt.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)
