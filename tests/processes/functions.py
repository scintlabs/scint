from enum import Enum
from typing import Dict

from src.processes.lib.functions import generate_model


if __name__ == "__main__":
    from typing import Optional, List, Union

    class Color(Enum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    def my_func(
        name: str,
        count: int,
        color: Color,
        tags: Optional[List[str]] = None,
        meta: Dict[str, Union[int, str]] = {},
    ):
        """
        This is a test function.

        Args:
            name: The name to use.
            count: How many times.
            color: A color choice.
            tags: A list of tags.
            meta: Arbitrary key-value metadata.
        """
        pass

    model = generate_model(my_func)
    import json

    print(json.dumps(model, indent=4))
