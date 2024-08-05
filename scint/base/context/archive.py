import uuid
from typing import List, Optional, Dict, Any, Tuple

import numpy as np

from .threads import Thread


class Node:
    def __init__(self, id: str, elements: List[Dict[str, Any]]):
        self.id = id
        self.elements = elements
        self.children: List[Node] = []
        self.parent: Optional[Node] = None

    def add_child(self, child: "Node"):
        self.children.append(child)
        child.parent = self


class ArchiveTree:
    def __init__(self):
        self.root: Optional[Node] = None

    def archive_thread(self, thread: Thread) -> str:
        new_node = Node(
            thread_id=str(uuid.uuid4()),
            messages=[msg.dict() for msg in thread.messages],
            metadata={
                "keywords": thread.keywords,
                "aggregate_embedding": thread.aggregate_embedding,
                "importance_score": thread.importance_score,
                "last_access_time": thread.last_access_time,
                "access_count": thread.access_count,
            },
        )

        if not self.root:
            self.root = new_node
        else:
            most_similar_node = self.find_most_similar_node(new_node)
            most_similar_node.add_child(new_node)

        return new_node.thread_id

    def find_most_similar_node(self, new_node: Node) -> Node:
        def similarity(node1: Node, node2: Node) -> float:
            emb1 = node1.metadata["aggregate_embedding"]
            emb2 = node2.metadata["aggregate_embedding"]
            return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

        def dfs(
            node: Node, best_node: Node, best_similarity: float
        ) -> Tuple[Node, float]:
            sim = similarity(node, new_node)
            if sim > best_similarity:
                best_node, best_similarity = node, sim

            for child in node.children:
                child_best, child_sim = dfs(child, best_node, best_similarity)
                if child_sim > best_similarity:
                    best_node, best_similarity = child_best, child_sim

            return best_node, best_similarity

        return dfs(self.root, self.root, 0)[0]

    def retrieve_thread(self, thread_id: str) -> Optional[Node]:
        def dfs(node: Node) -> Optional[Node]:
            if node.thread_id == thread_id:
                return node
            for child in node.children:
                result = dfs(child)
                if result:
                    return result
            return None

        return dfs(self.root) if self.root else None

    def search_archived_threads(
        self, query_embedding: np.ndarray, threshold: float = 0.7
    ):
        results = []

        def dfs(node: Node):
            similarity = np.dot(
                query_embedding, node.metadata["aggregate_embedding"]
            ) / (
                np.linalg.norm(query_embedding)
                * np.linalg.norm(node.metadata["aggregate_embedding"])
            )
            if similarity >= threshold:
                results.append(node)
            for child in node.children:
                dfs(child)

        dfs(self.root)
        return results
