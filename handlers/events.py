from core.memory import Message


def schedule_event():
    return Message("system", "Event scheduled.", "schedule_event")
