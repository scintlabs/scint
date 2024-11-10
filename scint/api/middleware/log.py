from falcon import Request, Response


class LoggingMiddleware:
    def __init__(self, logger=None):
        self.logger = logger

    async def process_response(self, req: Request, resp: Response) -> None:
        await self.logger.info(f"Request: {req.path} - Status: {resp.status}")
