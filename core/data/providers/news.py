import requests


def nytimes(topic: str = "world"):
    api_key = "7NKUxGlG9nEuayaoQXaCuqAVdHqbDmYf"
    url = f"https://api.nytimes.com/svc/topstories/v2/{topic}.json?api-key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)

    return response
