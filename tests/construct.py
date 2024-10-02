from typing import Dict, List

from scint.framework import Interface
from scint.framework.constructs.domains import Domain
from scint.framework.components import Link


class Construct(Interface):
    def __init__(self, context):
        super().__init__()
        self.domains: Dict[str, Domain] = {}
        self.links: Dict[str, List[Link]] = {}

    def add_domain(self, domain: Domain):
        self.domains[domain.name] = domain

    def add_link(self, anchor, ref, weight=1.0, title="", annotation=""):
        link = Link(self, anchor, ref, weight, title, annotation)
        if anchor not in self.links:
            self.links[anchor] = []
        self.links[anchor].append(link)

    def get_neighbors(self, node_name: str):
        return self.links.get(node_name, [])
