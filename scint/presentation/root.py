from scint.presentation.template import TemplateResource


class RootResource(TemplateResource):
    def __init__(self):
        super().__init__("root.html")

    async def on_get(self, req, resp):
        self.render(req, resp, title="Scint Chat")
