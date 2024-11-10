import falcon
import os
from jinja2 import Environment, FileSystemLoader

templates = os.path.join(os.path.dirname(__file__), "templates")
env = Environment(loader=FileSystemLoader(templates))


class Template:
    def __init__(self, template):
        self.template = template

    def render(self, req, resp, **kwargs):
        template = env.get_template(self.template)
        resp.content_type = falcon.MEDIA_HTML
        resp.text = template.render(**kwargs)
