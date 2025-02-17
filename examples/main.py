import asyncio

# from scint.framework.types.interfaces import Interface, Processor
from scint.lib.common.traits import Trait
from scint.lib.exchange import Exchange


class Loadable(Trait):
    async def load_image(self, image_name: str):
        """
        Use this function to load an image by name.

        Args:
                image_name: The name of the image to load.
        """
        return image_name

    async def load_doc(self, doc_name: str):
        """
        Use this function to load a document.

        Args:
                doc_name: The name of the document to edit.
        """
        return doc_name


# c = Chain([p1, p2])
# p = Process(ctx)
# p.add(c)
# ctx.messages.append({"role": "user", "content": "hi"})


async def main():
    # proc = Processor()
    # interface = Interface()
    router = Exchange()
    await router.start()

    req_id = router.route("sup")
    print(req_id)


if __name__ == "__main__":
    asyncio.run(main())
