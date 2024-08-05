import numpy as np
from typing import List, Dict, Optional
from collections import deque
import time

from scint.base.components.prompts import Message

EMBEDDING_SIZE = 1536


class Thread:
    def __init__(self):
        self.messages: List[Message] = []
        self.aggregate_embedding: np.ndarray = np.zeros(EMBEDDING_SIZE)
        self.labels: Dict[str, int] = {}
        self.next_thread: Optional["Thread"] = None
        self.prev_thread: Optional["Thread"] = None
        self.last_accessed: float = time.time()
        self.access_count: int = 0
        self.importance_score: float = 0.0

    def add_message(self, message: Message, embedding: np.ndarray, labels: List[str]):
        self.messages.append(message)
        self.update_aggregate_embedding(embedding)
        self.update_labels(labels)
        self.access_count += 1
        self.last_access_time = time.time()
        self.update_importance_score()

    def update_importance_score(self):
        time_factor = 1 / (time.time() - self.last_access_time + 1)
        access_factor = self.access_count
        content_factor = sum(self.labels.values())

        self.importance_score = (
            0.3 * time_factor + 0.4 * access_factor + 0.3 * content_factor
        )


class ThreadManager:
    def __init__(self, max_threads: int = 10):
        self.head: Optional[Thread] = None
        self.active_thread: Optional[Thread] = None
        self.thread_queue: deque = deque(maxlen=max_threads)
        self.max_threads = max_threads

    def add_message(self, message: Message, embedding: np.ndarray, labels: List[str]):
        if not self.head:
            self.head = Thread()
            self.active_thread = self.head
            self.thread_queue.append(self.head)
        else:
            most_similar_thread = self.find_most_similar_thread(embedding, labels)
            if self.should_create_new_thread(most_similar_thread, embedding, labels):
                new_thread = Thread()
                new_thread.prev_thread = most_similar_thread
                most_similar_thread.next_thread = new_thread
                self.active_thread = new_thread

                if len(self.thread_queue) == self.max_threads:
                    self.remove_least_important_thread()

                self.thread_queue.append(new_thread)
            else:
                self.active_thread = most_similar_thread

        self.active_thread.add_message(message, embedding, labels)
        self.update_thread_queue()

    def remove_least_important_thread(self):
        least_important = min(self.thread_queue, key=lambda t: t.importance_score)
        self.thread_queue.remove(least_important)
        # Update links
        if least_important.prev_thread:
            least_important.prev_thread.next_thread = least_important.next_thread
        if least_important.next_thread:
            least_important.next_thread.prev_thread = least_important.prev_thread

        if least_important == self.head:
            self.head = least_important.next_thread

    def update_thread_queue(self):
        # le-sort queue based on importance scores
        self.thread_queue = deque(
            sorted(self.thread_queue, key=lambda t: t.importance_score, reverse=True),
            maxlen=self.max_threads,
        )

    def update_aggregate_embedding(self, embedding: np.ndarray):
        # use exponential moving average to update the aggregate embedding
        alpha = 0.1  #  control weight of new messages
        self.aggregate_embedding = (
            1 - alpha
        ) * self.aggregate_embedding + alpha * embedding

    def update_labels(self, labels: List[str]):
        for keyword in labels:
            self.labels[keyword] = self.labels.get(keyword, 0) + 1

    def find_most_similar_thread(
        self, embedding: np.ndarray, labels: List[str]
    ) -> Thread:
        # TODO: implement logic to select thread by similarity
        pass

    def should_create_new_thread(
        self, thread: Thread, embedding: np.ndarray, labels: List[str]
    ) -> bool:
        # TODO: logic for determining new thread creation
        pass
