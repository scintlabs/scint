import rethinkdb

r = rethinkdb.RethinkDB()


class StorageController:
    """
    """
    def __init__(self, host="localhost", port=28015, db="scint"):
        self.conn = r.connect(host=host, port=port, db=db)
        self.db = db
        self.tables = ["context", "messages", "prompts", "functions"]

        for table in self.tables:
            if not r.table_list().contains(table).run(self.conn):
                r.table_create(table).run(self.conn)

    def save_message(self, context_name, message):
        """
        """
        data = {**message.model_dump()}
        r.table("messages").insert(data).run(self.conn)

    def load_messages(self, context_name):
        """
        """
        cursor = (
            r.table(self.table)
            .filter({"context_name": context_name})
            .order_by("timestamp")
            .run(self.conn)
        )
        return [message for message in cursor]

    def delete_messages(self, context_name):
        """
        """
        r.table(self.table).filter({"context_name": context_name}).delete().run(
            self.conn
        )

    def close(self):
        """
        """
        self.conn.close()


storage_controller = StorageController()
