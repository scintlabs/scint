from core.worker import Worker


get_weather = Worker(
    name="get_weather",
    purpose="You are a weather retrieval function for Scint, an intelligent assistant.",
    description="Use this function to get weather data for the specified city.",
    params={
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city name.",
            },
        },
    },
    req=["city"],
)
