import os
import env
import requests

nyt_api_key = env.get['nyt_api_key']

top_home = f'https://api.nytimes.com/svc/topstories/v2/home.json?api-key={nyt_api_key}'
top_world = 'https://api.nytimes.com/svc/topstories/v2/world.json?api-key=yourkey'
top_science = f'https://api.nytimes.com/svc/topstories/v2/science.json?api-key={nyt_api_key}'
top_arts = f'https://api.nytimes.com/svc/topstories/v2/arts.json?api-key={nyt_api_key}'
top_us = f'https://api.nytimes.com/svc/topstories/v2/us.json?api-key={nyt_api_key}'
 