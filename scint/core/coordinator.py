from scint.core.messages import Message
from scint.modules import persona, reading, writing, development, networking, system
from scint.services.logger import log


class Coordinator:
    def __init__(self):
        self.persona = persona.Scint()
        self.reading = reading.Reading()
        self.writing = writing.Composition()
        self.development = development.Development()
        self.web_browsing = networking.WebBrowsing()
        self.system = system.SystemManagement()

    async def process_request(self, message: Message):
        try:
            message = message
            pass

        except Exception as e:
            log.error(f"{self.__class__.__name__}: {e}")
            raise
