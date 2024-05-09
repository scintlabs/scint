import json
import psycopg2


class StorageController:
    def __init__(self):
        self.db_config = None
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_config)
            print("Connected to the database.")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Disconnected from the database.")

    def execute_query(self, query, params=None):
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                self.conn.commit()
                return cur.fetchall()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.execute_query(query)

    def insert_data(self, table_name, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        values = tuple(data.values())
        self.execute_query(query, values)

    def update_data(self, table_name, data, condition):
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        values = tuple(data.values())
        self.execute_query(query, values)

    def delete_data(self, table_name, condition):
        query = f"DELETE FROM {table_name} WHERE {condition}"
        self.execute_query(query)

    def select_data(self, table_name, columns, condition=None):
        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute_query(query)

    def store_json(self, json_data):
        query = "INSERT INTO json_store (data) VALUES (%s)"
        self.execute_query(query, (json.dumps(json_data),))

    def retrieve_json(self, json_id):
        query = "SELECT data FROM json_store WHERE id = %s"
        result = self.execute_query(query, (json_id,))
        if result:
            return json.loads(result[0][0])
        return None

    def search(self, query): ...

    def get_context(self, context_id): ...

    def update_context(self, context_id, context_data): ...


storage_controller = StorageController()
