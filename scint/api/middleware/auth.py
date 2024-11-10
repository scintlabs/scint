# api/middleware/base.py
from falcon import Request, Response


class AuthMiddleware:
    def __init__(self, service=None):
        self.auth_service = None

    async def process_request(self, req: Request, resp: Response) -> None:
        await req.get_header("Authorization")
