from scint.ensemble.components.enum import Enumerator


class Status:
    status = Enumerator(
        "ProcessStatus",
        {"started": {}, "waiting": {}, "failed": {}, "finding": {}, "stopped": {}},
    )
