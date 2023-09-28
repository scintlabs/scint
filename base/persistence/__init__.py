from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class LifeCycle(BaseModel):
    started_on: date = Field(default=date.today())
    updated_on: Optional[date] = None
    terminate_on: Optional[date] = None
    ended_on: Optional[date] = None

    @validator("updated_on", pre=True, always=True, check_fields=False)
    def validate_updated_on(cls, v, values):
        started_on = values.get("started_on")

        if started_on and v and v < started_on:
            raise ValueError("Updates must come after the starting date.")
        return v

    @validator("terminate_on", pre=True, always=True)
    def validate_terminate_on(cls, v, values):
        updated_on = values.get("updated_on") or values.get("started_on")

        if updated_on and v and v < updated_on:
            raise ValueError("The termination date must come after the latest update.")
        return v

    @validator("ended_on", pre=True, always=True)
    def validate_ended_on(cls, v, values):
        terminate_on = (
            values.get("terminate_on")
            or values.get("updated_on")
            or values.get("started_on")
        )
        if terminate_on and v and v < terminate_on:
            raise ValueError(
                "The end date must come after the last update or termination date."
            )
        return v
