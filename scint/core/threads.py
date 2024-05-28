import time

from scint.core.structures import Thread
from scint.modules.logging import log

import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class ThreadManager:
    def __init__(self):
        log.info(f"Initializing Thread Manager.")
        self.threads = []

    def get_thread(self, embedding):
        log.info(f"Getting thread for message.")
        if len(self.threads) == 0:
            return self.new_thread()
        else:
            for thread in self.threads:
                similarity = cosine_similarity(embedding, thread.messages[-1].embedding)
                if similarity > 0.9:
                    log.info(f"Found thread with {similarity} similarity.")
                    return thread
        return self.new_thread()

    def new_thread(self):
        log.info(f"Building new thread.")
        self.threads.append(Thread())
        return self.threads[-1]


thread_manager = ThreadManager()
