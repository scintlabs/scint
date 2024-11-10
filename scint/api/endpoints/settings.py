from falcon.asgi import Request, Response

from scint.context.settings import Settings


class SettingsResource:
    @staticmethod
    def __init__(self, logger=None):
        self.settings = Settings()

    async def process_response(self, req: Request, resp: Response) -> None:
        await self.logger.info(f"Request: {req.path} - Status: {resp.status}")
