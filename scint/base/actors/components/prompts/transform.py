transform = [
    {
        "name": "description",
        "data": [
            {
                "type": "text",
                "data": "Use the provided message to generate a detailed description and semantic labels that capture the essence and context of the text. These are notes between a language model and a user, source material for generating search indexes used to find and retrieve relevant contex, so precision and detail are key. Format your response as a JSON object with a `description` and `labels` keys. The `description` should be a valid string while the labels should be an array of strings.",
            }
        ],
        "labels": {"data": ["context description", "classification", "retrieval"]},
    },
    {
        "name": "summary",
        "type": "prompt",
        "discriptions": [
            "Creating concise summaries.",
            "Capturing the essence of responses.",
            "Providing brief self notes.",
        ],
        "categories": ["generator"],
        "labels": [
            "summary",
            "concise",
            "brief",
            "first-person",
            "self notes",
            "essence",
            "overview",
        ],
        "data": [
            {
                "type": "text",
                "data": "Summarize responses from the assistant in the form of brief self notes. Summaries should capture the essence of the response using first-person perspective. Write like Hemingway on a speed run.",
            }
        ],
    },
]
