import json

import psycopg2
import psycopg2.extras

from scint.services import Service


__all__ = "Persistence"


class Persistence(Service):
    def __init__(self):
        super().__init__()

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

    def search_documents(self, **kwargs):
        try:
            self.connect()
            self.cursor.execute(
                """
                    SELECT * FROM search_documents(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            print("Error while searching documents:", error)
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
                    "INSERT INTO documents (id, title, body, embedding, category, document_type, metadata, path) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                    "ON CONFLICT (id) DO UPDATE SET "
                    "title = EXCLUDED.title, body = EXCLUDED.body, embedding = EXCLUDED.embedding, "
                    "category = EXCLUDED.category, document_type = EXCLUDED.document_type, "
                    "metadata = EXCLUDED.metadata, path = EXCLUDED.path",
                    (
                        key,
                        value.title,
                        value.body,
                        value.embedding,
                        value.category,
                        value.document_type,
                        json.dumps(value.metadata),
                        value.path,
                    ),
                )

            for key, value in self.links.items():
                self.cursor.execute(
                    "INSERT INTO edges (id, from_id, to_id, relationship_type, weight) "
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
            self.cursor.execute("SELECT * FROM documents")
            for row in self.cursor.fetchall():
                self.graph.add_value(
                    id=row["id"],
                    title=row["title"],
                    body=row["body"],
                    embedding=list(row["embedding"]),
                    category=row["category"],
                    document_type=row["document_type"],
                    metadata=row["metadata"],
                    path=row["path"],
                )

            self.cursor.execute("SELECT * FROM edges")
            for row in self.cursor.fetchall():
                self.graph.add_edge(
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
