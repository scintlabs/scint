import os, math

import scrapy
from sentence_transformers import util
from sentence_transformers import SentenceTransformer

from util.logging import logger

filepath = os.getcwd()
with open(filepath, encoding="utf-8") as f:
    content = f.read()


async def similarity_search(query):
    """Search files/embeddings with SentenceTransformer."""
    model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-cos-v1")
    logger.info(f"Searching embeddings.")
    query_embedding = model.encode(query)
    results = {}

    for file_path, embeddings in index.items():
        for idx, embedding in enumerate(embeddings):
            similarity_score = util.cos_sim(query_embedding, embedding)
            current_file_score = results.get(file_path, {}).get("score", 0)
            if similarity_score > current_file_score:
                results[file_path] = {"score": similarity_score, "chunk_idx": idx}

    contextual_data = {}

    for file_path, data in results.items():
        chunk_idx = data["chunk_idx"]
        chunk = content[file_path][chunk_idx]
        contextual_data[file_path] = {"score": data["score"], "context": chunk}

        sorted_results = sorted(
            contextual_data.items(), key=lambda item: item[1]["score"], reverse=True
        )

    for file_path, data in sorted_results:
        print(f"Match in {file_path}:")
        print(data["context"])
        print("------")

        return sorted_results


def cosine_similarity(vec_a, vec_b):
    if not vec_a or len(vec_a) != len(vec_b):
        raise ValueError(
            "Vectors for cosine similarity must be non-empty and of the same size."
        )

    dot_product = 0
    norm_a = 0
    norm_b = 0
    for i in range(len(vec_a)):
        dot_product += vec_a[i] * vec_b[i]
        norm_a += vec_a[i] ** 2
        norm_b += vec_b[i] ** 2

    return (
        0
        if norm_a == 0 or norm_b == 0
        else dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))
    )
