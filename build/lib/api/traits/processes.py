from scint.api.types import Trait


class Executable(Trait):
    async def execute(self, *args, **kwargs):
        response = await self.callback(*args, **kwargs)
        if self.publish:
            return await self.publish(response)


class Runnable(Trait):
    async def run(self):
        while self.current_component_index < len(self.components):
            component = self.components[self.current_component_index]
            result = await component.evaluate(self)
            if result == "break":
                break
            self.current_component_index += 1


class Splittable(Trait):
    async def split(self):
        new_process = self.clone()
        return [self, new_process]

    async def clone(self):
        return self.deepcopy()


class Sequencable(Trait):
    pass


class Branchable(Trait):
    async def evaluate(self):
        result = self.result
        if result:
            pass
        elif not result:
            pass
        else:
            pass
