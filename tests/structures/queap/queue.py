from collections import deque

from .tree import Tree


class Queue:
    def __init__(self):
        self.queues = []
        self.size = 0

    def push(self, item, priority):
        while priority >= len(self.queues):
            self.queues.append(deque())

        self.queues[priority].append(item)
        self.size += 1

    def pop(self):
        if self.size == 0:
            raise IndexError("Queap is empty")

        for priority in range(len(self.queues) - 1, -1, -1):
            if self.queues[priority]:
                self.size -= 1
                return self.queues[priority].popleft()

    def peek(self):
        if self.size == 0:
            raise IndexError("Queap is empty")

        for priority in range(len(self.queues) - 1, -1, -1):
            if self.queues[priority]:
                return self.queues[priority][0]

    def __len__(self):
        return self.size

    def __bool__(self):
        return self.size > 0
