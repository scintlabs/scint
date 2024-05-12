import psycopg2
import redis
from rethinkdb import RethinkDB

r = RethinkDB()


class RedisConnectionManager:
    def __init__(self, host="localhost", port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connection = None

    def get_connection(self):
        if not self.connection:
            self.connect()
        return self.connection

    def connect(self):
        self.connection = redis.Redis(host=self.host, port=self.port, db=self.db)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None


class PostgresConnectionManager:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            self.cursor = self.connection.cursor()
            print("Connected to the PostgreSQL database successfully!")
        except (psycopg2.Error, Exception) as error:
            print(f"Error while connecting to PostgreSQL: {error}")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("PostgreSQL connection closed.")
