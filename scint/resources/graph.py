import falcon.asgi
import json


class Node:
    def __init__(self, id, label, type):
        self.id = id
        self.label = label
        self.type = type


class Edge:
    def __init__(self, source, target, type):
        self.source = source
        self.target = target
        self.type = type


class GraphResource:
    def __init__(self):
        self.nodes = []
        self.edges = []

    async def on_get(self, req, resp):
        graph = {
            "nodes": [vars(node) for node in self.nodes],
            "edges": [vars(edge) for edge in self.edges],
        }
        resp.text = json.dumps(graph)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200

    async def on_post(self, req, resp):
        data = await req.get_media()
        if "node" in data:
            node = Node(**data["node"])
            self.nodes.append(node)
        elif "edge" in data:
            edge = Edge(**data["edge"])
            self.edges.append(edge)
        resp.status = falcon.HTTP_201

    async def on_get_html(self, req, resp):
        resp.content_type = falcon.MEDIA_HTML
        with open("scint/resources/views/graph.html", "r") as f:
            resp.text = f.read()


app = falcon.asgi.App()
graph_resource = GraphResource()
app.add_route("/graph", graph_resource)
app.add_route("/", graph_resource, suffix="html")  # New route for HTML
