from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from base.observability.logging import logger


class EventHandler(FileSystemEventHandler):
    def __init__(self, parser):
        self.parser = parser

    def on_modified(self, event):
        logger.info(f"File {event.src_path} has been modified")
        self.parser.process_file(event.src_path)
