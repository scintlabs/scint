from scint.base.types.components import Components


class SwitchComponent(Components):
    on = False

    async def switch(self, toggle: bool):
        self.running = toggle
        if self.running:
            await self.start()

    def __set__(self, on: bool):
        if on and not self.on:
            print("Turning on.")
        elif not on and self.on:
            print("Shuttind down.")
        elif on and self.on:
            return AttributeError("Already running.")
        elif not on and not self.on:
            return AttributeError("Not running.")
