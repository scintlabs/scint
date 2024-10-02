from scint.framework.components import Component


class Start(Component):
    async def start(self):
        while self.current_component_index < len(self.components):
            component = self.components[self.current_component_index]
            result = await component.evaluate(self)
            if result == "break":
                break
            self.current_component_index += 1


class Split(Component):
    async def split(self):
        new_process = self.clone()
        return [self, new_process]

    async def clone(self):
        return self.deepcopy()

    async def evaluate(self):
        pass


class Sequence(Component):
    pass


class Fallback(Component):
    pass


class Branch(Component):
    async def evaluate(self):
        result = self.result
        if result:
            pass
        elif not result:
            pass
        else:
            pass
