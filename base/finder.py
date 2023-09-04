import os

import scrapy
from scrapy_splash import SplashRequest
from sentence_transformers import util

from util.logging import logger

filepath = os.getcwd()
with open(filepath, encoding="utf-8") as f:
    content = f.read()

# Add Splash server URL
SPLASH_URL = "http://localhost:8050"

# Add Splash to the Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
    "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
}

# Set a custom DUPEFILTER_CLASS
DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"

# Specify the SPLASH cache arguments
HTTPCACHE_STORAGE = "scrapy_splash.SplashAwareFSCacheStorage"


class AIWikipediaSpider(scrapy.Spider):
    name = "ai_wikipedia"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Artificial_intelligence"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={"wait": 2})

    def parse(self, response):
        # Extract the main headings
        headings = response.css("span.mw-headline::text").getall()
        for heading in headings:
            yield {"heading": heading}


async def similarity_search(self, query):
    """Search files/embeddings with SentenceTransformer."""
    logger.info(f"Searching embeddings.")
    query_embedding = self.model.encode(query)
    results = {}

    for file_path, embeddings in self.index.items():
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
