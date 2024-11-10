import json

import psycopg2
import psycopg2.extras

from scint.repository.models.base import Model
from scint.repository.models.struct import Struct


class Persistence:
    def __init__(self, params):
        super().__init__(params)
        self.params = None
        self.domains = None
        self.links = None
        self.domains = None
        self.domains = None
        self.links = None
        self.params = None
        self.domains = None
        self.connection = None
        self.cursor = None
        self.collections = Struct()

    def connect(self):
        self.connection = psycopg2.connect(**self.params)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def disconnect(self):
        self.cursor.close()
        self.connection.close()

    def sync(self):
        self.connect()
        self.sync_to_db()
        self.sync_from_db()
        self.disconnect()

    def sync_to_db(self):
        self.connect()
        for domain in self.domains.values():
            self.cursor.execute(
                """
                INSERT INTO domains (id, name, description, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                embedding = EXCLUDED.embedding
                RETURNING id
                """,
                (
                    domain.id,
                    domain.name,
                    domain.description,
                    domain.embedding,
                ),
            )
            domain.id = self.cursor.fetchone()[0]

        for collection in self.collections.__dict__.items():
            self.cursor.execute(
                """
                INSERT INTO collections (id, title, description, collection, embedding, domain_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                collection = EXCLUDED.collection,
                embedding = EXCLUDED.embedding,
                domain_id = EXCLUDED.domain_id
                RETURNING id
                """,
                (
                    collection.id,
                    collection.title,
                    collection.description,
                    json.dumps(collection.collection),
                    collection.embedding,
                    collection.domain_id,
                ),
            )
            collection.id = self.cursor.fetchone()[0]

        for link in self.links.values():
            self.cursor.execute(
                """
                INSERT INTO links (id, title, anchor, reference, weight, annotation)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                anchor = EXCLUDED.anchor,
                reference = EXCLUDED.reference,
                weight = EXCLUDED.weight,
                annotation = EXCLUDED.annotation
                RETURNING id
                """,
                (
                    link.id,
                    link.title,
                    link.anchor,
                    link.reference,
                    link.weight,
                    link.annotation,
                ),
            )
            link.id = self.cursor.fetchone()[0]
        self.connection.commit()
        self.disconnect()

    def sync_from_db(self):
        self.connect()
        self.cursor.execute("SELECT * FROM domains")

        self.cursor.execute("SELECT * FROM collections")
        for row in self.cursor.fetchall():
            collection = Model.Bundle(
                title=row["title"],
                description=row["description"],
                collection_data=row["collection"],
            )
            collection.id = row["id"]
            collection.embedding = list(row["embedding"])
            collection.domain_id = row["domain_id"]
            self.collections[collection.id] = collection

            if collection.domain_id in self.domains:
                self.domains[collection.domain_id].add_collection(collection)

        self.disconnect()

    def search_collections(self, **kwargs):
        self.connect()
        self.cursor.execute(
            """
            SELECT * FROM search_collections(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                kwargs.get("query_text"),
                kwargs.get("query_embedding"),
                kwargs.get("match_count", 30),
                kwargs.get("rrf_k", 0.5),
                kwargs.get("fuzzy_weight", 0.2),
                kwargs.get("fts_title_weight", 0.3),
                kwargs.get("fts_description_weight", 0.3),
                kwargs.get("semantic_weight", 0.2),
                kwargs.get("max_graph_distance", 2),
            ),
        )
        results = self.cursor.fetchall()
        processed_results = []
        for row in results:
            result = dict(row)
            result["embedding"] = list(result["embedding"])
            processed_results.append(result)
        self.disconnect()
        return processed_results


__all__ = "Persistence"
