from scint.workers.worker import Worker
from scint.workers.prompts import base_init, base_status, prism_init


scint = Worker("scint", prism_init, base_status, target=None)
team = {"scint": scint}
