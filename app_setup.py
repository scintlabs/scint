from core.persona import Persona
from workers.web_browser import search_web, load_website
from workers.api_parser import get_weather

persona = Persona()
persona.coordinator.add_workers(
    search_web,
    load_website,
    get_weather,
)
