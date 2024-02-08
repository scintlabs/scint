# Scint Search

``` bash
poetry install
tailwindcss -i static/styles/tailwind.css -o static/styles/index.css --watch &
poetry run uvicorn app:main --reload --reload-dir=templates --reload-dir=static
```

```
redis-stack-server
redisinsight
```
