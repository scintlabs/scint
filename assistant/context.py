import json
import psycopg2


import os


class Context:
    def __init__(self):
        self.buffers = {}
        self.current_buffer = None

    def load_file(self, filepath):
        # Check if the file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file: '{filepath}'")

        # Read the file in chunks
        with open(filepath, "r") as f:
            content = f.read()

        # Split the content into chunks
        chunks = self.chunk_content(content)

        # Store the chunks in a buffer
        buffer_id = len(self.buffers)
        self.buffers = chunks

        # Set this buffer as the current one
        self.current_buffer = buffer_id

    def chunk_content(self, content, chunk_size=1000):
        # This method splits the content into chunks
        return [content for i in range(0, len(content), chunk_size)]

    def get_current_chunk(self):
        # This method returns the current chunk from the current buffer
        if self.current_buffer is None:
            raise Exception("No buffer loaded")

        return self.buffers[0]

    def preprocess(self, message):
        # Add the current chunk to the message
        chunk = self.get_current_chunk()
        message += "\n\n" + chunk
        return message

    def postprocess(self, message):
        # Do nothing for now
        return message


# def connect_to_db():
#     connection = psycopg2.connect(
#         user="buftype_context",
#         password="secretagentman",
#         host="localhost",
#         port="5432",
#         database="buftype",
#     )

#     try:
#         cursor = connection.cursor()
#         print(connection.get_dsn_parameters(), "\n")
#         cursor.execute("SELECT version();")
#         record = cursor.fetchone()

#         print("You are connected to - ", record, "\n")

#     except (Exception, psycopg2.Error) as error:
#         print("Error while connecting to PostgreSQL", error)
#     finally:
#         if connection:
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")


# connect_to_db()
