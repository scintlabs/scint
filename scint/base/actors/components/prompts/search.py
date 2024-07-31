search = {
    "name": "github_repos",
    "type": "function",
    "description": "Searches GitHub repositories using the specified query and yields the search results.",
    "categories": ["search"],
    "labels": ["GitHub", "repository search", "search", "query", "repos"],
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query string.",
            }
        },
        "required": ["query"],
    },
}
