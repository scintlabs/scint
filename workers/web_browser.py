from core.worker import Worker


search_web = Worker(
    name="search_web",
    purpose="You are a web search function for Scint, an intelligent assistant.",
    description="Use this function to search the web.",
    params={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The string to search the web for.",
            },
        },
    },
    req=["query"],
)

load_website = Worker(
    name="load_website",
    purpose="You are a website parsing function for Scint, an intelligent assistant.",
    description="Use this function to get website data from a URL.",
    params={
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The URL of the website to parse.",
            },
        },
    },
    req=["url"],
)
