import json
from typing import Dict

import psycopg2
import psycopg2.extras

from scint.framework.collections.collection import Collection
from scint.framework.entities.service import Service
from scint.framework.models import Link
from scint.app.data.domains import Domain


__all__ = "Persistence"


class Persistence(Service):
    def __init__(self, context, params):
        super().__init__()
        self.params = params
        self.collections: Dict[int, Collection] = {}
        self.domains: Dict[int, Domain] = {}
        self.links: Dict[int, Link] = {}

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

        for collection in self.collections.values():
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
        for row in self.cursor.fetchall():
            domain = Domain(name=row["name"], description=row["description"])
            domain.id = row["id"]
            domain.embedding = list(row["embedding"])
            self.domains[domain.id] = domain

        self.cursor.execute("SELECT * FROM collections")
        for row in self.cursor.fetchall():
            collection = Collection(
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

        self.cursor.execute("SELECT * FROM links")
        for row in self.cursor.fetchall():
            link = Link(
                title=row["title"],
                anchor=row["anchor"],
                reference=row["reference"],
                weight=row["weight"],
                annotation=row["annotation"],
            )
            link.id = row["id"]
            self.links[link.id] = link

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
