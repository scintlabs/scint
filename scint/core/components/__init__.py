from uuid import uuid4
from pydantic import Field
import json
import psycopg2

from scint.core import BaseType


class Component(metaclass=BaseType):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: str = Field(default_factory=lambda: str(uuid4()))

        for name, value in kwargs.items():
            setattr(self, name, value)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Process(metaclass=BaseType):
    def __init__(self, composition):
        self.id: str = Field(default_factory=lambda: str(uuid4()))
        self.composition = composition

    async def evaluate(self):
        async with self.context() as ctx:
            return await ctx.app.services.intelligence.process(self.composition)


class Construct(metaclass=BaseType):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Composition(metaclass=BaseType):
    def __init__(self, **kwargs):
        self.id: str = Field(default_factory=lambda: str(uuid4()))
        self.messages = []
        for name, value in kwargs.items():
            setattr(self, name, value)

        self.db_params = {
            "dbname": "scint",
            "user": "kaechle",
            "password": "scint",
            "host": "localhost",
            "port": 5432,
        }

        self.search_args = {
            "query": None,
            "embedding": None,
            "matches": 30,
            "rrf_k": 0.5,
            "fuzzy_weight": 0.2,
            "title_weight": 0.3,
            "body_weight": 0.3,
            "semantic_weight": 0.2,
            "category": None,
            "doc_type": None,
            "path": None,
            "graph_distance": 2,
        }

        self.insert_args = {
            "title": None,
            "body": None,
            "embedding": None,
            "category": None,
            "doc_type": None,
            "metadata": None,
            "path": None,
        }

    def connect(self):
        self.connection = psycopg2.connect(**self.db_params)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def search_compositions(self, **kwargs):
        try:
            self.connect()
            self.cursor.execute(
                """
                    SELECT * FROM search_compositions(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                tuple(self.search_args.values()),
            )
            results = self.cursor.fetchall()
            processed_results = []
            for row in results:
                result = dict(row)
                result["embedding"] = list(result["embedding"])
                processed_results.append(result)
            return processed_results
        except (Exception, psycopg2.Error) as error:
            print("Error while searching compositions:", error)
            return []
        finally:
            self.disconnect()

    def sync(self):
        self.sync_to_db()
        self.sync_from_db()

    def sync_to_db(self):
        try:
            self.connect()
            for key, value in self.compositions.items():
                self.cursor.execute(
                    "INSERT INTO compositions (id, title, body, embedding, category, composition_type, metadata, path) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET "
                    "title = EXCLUDED.title, body = EXCLUDED.body, embedding = EXCLUDED.embedding, "
                    "category = EXCLUDED.category, composition_type = EXCLUDED.composition_type, "
                    "metadata = EXCLUDED.metadata, path = EXCLUDED.path",
                    (
                        key,
                        value.title,
                        value.body,
                        value.embedding,
                        value.category,
                        value.composition_type,
                        json.dumps(value.metadata),
                        value.path,
                    ),
                )

            for key, value in self.links.items():
                self.cursor.execute(
                    "INSERT INTO links (id, from_id, to_id, relationship_type, weight) "
                    "VALUES (%s, %s, %s, %s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET "
                    "from_id = EXCLUDED.from_id, to_id = EXCLUDED.to_id, "
                    "relationship_type = EXCLUDED.relationship_type, weight = EXCLUDED.weight",
                    (
                        key,
                        value.from_id,
                        value.to_id,
                        value.relationship_type,
                        value.weight,
                    ),
                )

            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error while syncing to database:", error)
            self.connection.rollback()
        finally:
            self.disconnect()

    def sync_from_db(self):
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM compositions")
            for row in self.cursor.fetchall():
                self.graph.add_value(
                    id=row["id"],
                    title=row["title"],
                    body=row["body"],
                    embedding=list(row["embedding"]),
                    category=row["category"],
                    type=row["type"],
                    metadata=row["metadata"],
                    path=row["path"],
                )

            self.cursor.execute("SELECT * FROM links")
            for row in self.cursor.fetchall():
                self.graph.add_link(
                    id=row["id"],
                    from_id=row["from_id"],
                    to_id=row["to_id"],
                    relationship_type=row["relationship_type"],
                    weight=row["weight"],
                )
        except (Exception, psycopg2.Error) as error:
            print("Error while syncing from database:", error)
        finally:
            self.disconnect()

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        obj.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
