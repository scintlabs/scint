import asyncio

from scint.base.types.components import ComponentType, Enumerator, Queue


# TODO: https://en.wikipedia.org/wiki/Work_stealing

# One example where a deque can be used is the work stealing algorithm.[9] This algorithm implements task scheduling for several processors. A separate deque with threads to be executed is maintained for each processor. To execute the next thread, the processor gets the first element from the deque (using the "remove first element" deque operation). If the current thread forks, it is put back to the front of the deque ("insert element at front") and a new thread is executed. When one of the processors finishes execution of its own threads (i.e. its deque is empty), it can "steal" a thread from another processor: it gets the last element from the deque of another processor ("remove last element") and executes it. The work stealing algorithm is used by Intel's Threading Building Blocks (TBB) library for parallel programming.


def set_queues(queues):
    return Queue(queues)


def set_enum(states):
    state = Enumerator
    for key, value in states.items():
        setattr(state, key, value)
    return state


class Routine(metaclass=ComponentType):
    def __init__(self):
        super().__init__()
        self.running = False

    def switch(self, command: bool):
        self.running = command
        if self.running:
            asyncio.run(self.run())

    async def start(self, routine):
        while self.running:
            if self.queue.instructions:
                instruction_set = await self.queues.instructions.get()
                await self.build(instruction_set)

    # async def build(self, instruction_set: InstructionSet):
    #     self.load_subroutines(instruction_set.subroutines)
    #     for subroutine in self.subroutines():
    #         await subroutine()
    #


class Subroutine(Routine):
    def __init__(self):
        super().__init__()

    async def process(self, task):
        await self.queues.clarify.put(task.model_dump_json())
