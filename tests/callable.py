import asyncio
from scint.modules.components.handler import completion
from scint.support.logging import log

paragraph = """Metaprogramming refers to the technique of writing programs that can manipulate other programs, or even manipulate themselves, as part of their execution process. This advanced programming concept is widely used in various programming languages to achieve greater flexibility and to reduce code redundancy. For example, in languages like Python, decorators and metaclasses provide powerful tools for modifying the behavior of classes and functions at runtime. Similarly, in C++, templates allow for operations on generic types, enabling programmers to write more general and reusable code components. Metaprogramming can greatly enhance the adaptability of software, allowing it to dynamically alter its behavior based on external conditions or user inputs. However, it also introduces complexity and can make the code harder to understand and maintain. Thus, while metaprogramming offers significant advantages, it requires careful design and consideration to avoid potential pitfalls such as increased debugging difficulty and performance overhead."""


@completion(
    "Summarize this into one sentence, written in first person as you're describing a message you wrote to the user."
)
async def get_content(paragraph: str):
    yield paragraph


async def run_async_loop():
    generator = get_content(paragraph)
    async for i in generator:
        log.info(i)


async def run():
    tasks = [run_async_loop()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run())
