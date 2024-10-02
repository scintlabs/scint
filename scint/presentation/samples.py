from scint.app.presentation.template import TemplateResource


class BlogPost(TemplateResource):
    def __init__(self):
        super().__init__("blog.html")

    async def on_get(self, req, resp):
        self.render(req, resp, title="Scint Chat")


class MainPage(TemplateResource):
    def __init__(self):
        super().__init__("<h1>Welcome to Synapsia!</h1>")

    async def on_get(self, req, resp):
        self.render(req, resp, title="Scint Chat")
