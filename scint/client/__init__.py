import asyncio


from scint.lib.exchange import Exchange
from scint.lib.intelligence import Intelligent
from scint.lib.context import Contextual
from scint.lib.entities import Interpreter
from scint.lib.schema.threads import Message
from scint.lib.common.tools import Tools


exchange = Exchange()


class Loadable(Tools):
    async def load_image(self, image_name: str):
        """
        Use this function to load an image by name.
        image_name: The name of the image to load.
        """
        return image_name

    async def load_doc(self, doc_name: str):
        """
        Use this function to load a document.
        doc_name: The name of the document to edit.
        """
        return doc_name


async def main():
    interpreter = Interpreter()
    interpreter.traits(Contextual, Intelligent)
    interpreter.tools(Loadable)

    message = Message(
        content="The functions you have access to are the functions on the actual class. Can you name them for me?"
    )

    interpreter.context.messages.append(message)
    print(interpreter.model)


if __name__ == "__main__":
    asyncio.run(main())
