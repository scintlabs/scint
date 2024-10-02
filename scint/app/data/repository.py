from scint.app.data.domains import Domain
from scint.framework import Interface
from scint.framework.collections.collection import Collection
from scint.framework.components.function import Function
from scint.framework.models.messages import Message
from scint.framework.utils.helpers import cosine_similarity
from scint.framework.models.messages import InputMessage, Prompt


class Repository(Interface):
    def __init__(self, context):
        super().__init__(context)

    def add_domain(self, domain: Domain):
        self.construct.add_domain(domain)

    def add_collection(self, collection):
        domain = self._find_domain(collection)
        domain.add_collection(collection)

    def add_link(self, anchor, ref, weight=1.0, title="", annotation=""):
        self.construct.add_link(anchor, ref, weight, title, annotation)

    def select_domain_and_collection(self, message: Message):
        domain = None
        domain_similarity = -1
        for domain in self.construct.domains.values():
            domain_similarity = cosine_similarity(message.embedding, domain.embedding)
            if domain_similarity > domain_similarity:
                domain_similarity = domain_similarity
                domain = domain

        if domain is None or domain_similarity < 0.7:
            domain = Domain()
            domain.labels = message.labels
            domain.embedding = message.embedding
            self.construct.add_domain(domain)

    def select_collection(self, domain, message: Message):
        collection = None
        collection_similarity = -1
        for collection in domain.collections.values():
            collection_similarity = cosine_similarity(
                message.embedding, collection.embedding
            )
            if collection_similarity > collection_similarity:
                collection_similarity = collection_similarity
                collection = collection

        if collection is None or collection_similarity < 0.7:
            new_collection_name = "Collection for " + ", ".join(message.labels)
            collection = Collection(new_collection_name, items=[])
            collection.labels = message.labels
            collection.embedding = message.embedding
            domain.add_collection(collection)
        return collection

    def observe_and_modify(self):
        for domain in self.construct.domains.values():
            collections_to_reassign = []
            for collection in domain.collections.values():
                similarity = cosine_similarity(domain.embedding, collection.embedding)
                if similarity < 0.5:
                    collections_to_reassign.append(collection)
            for collection in collections_to_reassign:
                del domain.collections[collection.name]
                self.add_collection(collection)
            domain.embedding = domain.calculate_embedding()

    def _find_domain(self, collection: Collection):
        domain = None
        best_similarity = -1
        for domain in self.construct.domains.values():
            similarity = cosine_similarity(domain.embedding, collection.embedding)
            if similarity > best_similarity:
                best_similarity = similarity
                domain = domain
        if domain is None or best_similarity < 0.7:
            domain = Domain()
            domain.embedding = collection.embedding
            self.construct.add_domain(domain)
        return domain

    async def compose(self, message: InputMessage):
        self.compositions.messages.append(message)
        self.compositions.prompts = await self.compose_prompts("framework")
        self.compositions.functions = await self.compose_functions("framework")
        behavior = self.behaviors.select_behavior("respond")
        return await self.compose_process(behavior, self.composition)

    async def compose_process(self, behavior, composition):
        process = self.processes.select_process(1)
        self.processes.update_process(process, behavior, composition)
        return await self.processes.start_process(process)

    async def compose_prompts(self, message: InputMessage):
        prompts = []
        results = await self.search.results("prompts", "framework")
        for result in results:
            result.pop("id")
            prompts.append(Prompt(**result))
        return prompts

    async def compose_functions(self, message: InputMessage):
        functions = []
        results = await self.search.results("functions", "framework")
        for result in results:
            result.pop("id")
            functions.append(Function(**result))
        return functions
