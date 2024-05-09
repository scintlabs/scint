from redis import Redis
from rethinkdb import RethinkDB

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from injector import Injector, Module, Binder, SingletonScope

from scint.controllers.intelligence import IntelligenceController
from scint.controllers.context import ContextController
from scint.controllers.search import SearchController
from scint.controllers.storage import StorageController
from scint.support.types import Any, Dict


rethink = RethinkDB
redis = Redis

OpenAI = AsyncOpenAI
Anthropic = AsyncAnthropic
