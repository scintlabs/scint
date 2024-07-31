image = {
    "description": "Use this function to view images when the user requests feedback on an image in link format.",
    "categories": ["core"],
    "labels": ["image", "view", "link", "image url", "image viewer"],
    "parameters": {
        "type": "object",
        "properties": {
            "image_url": {
                "type": "string",
                "description": "The image url provided by the user.",
            }
        },
        "required": ["image_url"],
    },
}
