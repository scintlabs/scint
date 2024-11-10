from dataclasses import dataclass

from scint.repository.models.base import Model


@dataclass
class Channel(Model):
    channel_name = None
    subscribers = None

    def load(self, channel_name):
        self.channel_name = channel_name
        self.subscribers = set()
