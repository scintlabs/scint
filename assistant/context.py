import json
import psycopg2
import os


class Context:
    def __init__(self):
        self.buffers = {}
        self.current_buffer = None

    def load_file(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file: '{filepath}'")

        with open(filepath, "r") as f:
            content = f.read()

        chunks = self.chunk_content(content)

        buffer_id = len(self.buffers)
        self.buffers = chunks
        self.current_buffer = buffer_id

    def chunk_content(self, content, chunk_size=1000):
        return [content for i in range(0, len(content), chunk_size)]

    def get_current_chunk(self):
        if self.current_buffer is None:
            raise Exception("No buffer loaded")

        return self.buffers[0]

    def preprocess(self, message):
        chunk = self.get_current_chunk()
        message += "\n\n" + chunk
        return message

    def postprocess(self, message):
        # Do nothing for now
        return message
