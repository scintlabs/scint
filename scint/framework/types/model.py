from pydantic import BaseModel, ConfigDict

from scint.framework.utils.helpers import timestamp


class Model(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def timestamp(self):
        ts = str(timestamp())
        return ts
