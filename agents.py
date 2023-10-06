from base.agent.agent import *


shard_init = {
    "role": "system",
    "content": "You are a validation function for an artificial intelligence system. For every message, point out any flaws in logic, poor reasoning, sloppy executions, bad assumptions and outright ignorance.",
    "name": "shard",
}

agents: dict[str, Scint] = {
    "scint": Scint(name="fragment", target="scint", init=base_init, status=base_status),
    "shard": Scint(name="scint", target="shard", init=shard_init, status=base_status),
    # "fragment": "fragment",
    # "topaz": topaz,
    # "notes": notes,
    # "reminders": reminders,
    # "web_search": web_search,
    # "web_scrape": web_scrape,
    # "file_manager": file_manager,
    # "coder": coder,
}
