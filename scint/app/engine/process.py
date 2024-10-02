from scint.framework.compositions.process import Process
from scint.framework.models.responses import BehaviorsEnum
from scint.framework.entities.composer import Composer


class Intentions(Composer):
    def __init__(self):
        self.intent_behavior_map = {}

    def get_behavior(self, intent):
        return self.intent_behavior_map.get(intent, BehaviorsEnum.INTERACT)


class Behaviors(Composer):
    def __init__(self, context, *args, **kwargs):
        super().__init__(context, *args, **kwargs)


class Processes(Composer):
    def __init__(self, context, *args, **kwargs):
        super().__init__(context, *args, **kwargs)
        self.pid_count = -1
        self.behaviors = Behaviors(context)

    def create_process(self, context):
        self.pid_count += 1
        process = Process(context, self.pid_count)
        return self.compositions.create_composition(process)

    def select_process(self, pid):
        return self.compositions[pid] if self.compositions[pid] else None

    def update_process(self, process, behavior, composition):
        setattr(process, "core", behavior)
        setattr(process, "composition", composition)

    async def start_process(self, process):
        while self.current_component_index < len(self.components):
            component = self.components[self.current_component_index]
            result = await component.evaluate(self)
            if result == "break":
                break
            self.current_component_index += 1
