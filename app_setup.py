from core.assistant import Assistant
from core.persona import Persona
from workers.web_browser import search_web, load_website
from workers.api_parser import get_weather
from workers.file_manager import file_manager
from workers.event_manager import event_manager


assistant = Assistant()
persona = Persona()
persona.coordinator.add_workers(
    event_manager,
    file_manager,
    search_web,
    load_website,
    get_weather,
)
