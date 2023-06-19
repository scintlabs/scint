import json
import psycopg2


class Context:
    def __init__(self):
        self.last_known = None

    def buffer(self, message):
        self.buffer = []

    def database(self, database):
        self.database = database


def connect_to_db():
    connection = psycopg2.connect(
        user="cogiter_context",
        password="secretagentman",
        host="localhost",
        port="5432",
        database="cogiter",
    )

    try:
        cursor = connection.cursor()
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("SELECT version();")
        record = cursor.fetchone()

        print("You are connected to - ", record, "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


connect_to_db()
