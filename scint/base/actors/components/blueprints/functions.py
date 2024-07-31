from scint.base.types.providers import request_completion
from scint.base.models.messages import Message


def validate_metadata(self, func):
    for obj in self.metadata:
        if obj.get("name") == func.__name__:
            func.metadata = obj
    return func


async def generate_specification(description):
    yield Message()


async def generate_function(message):
    specification = await generate_specification(message)
    res = await request_completion([message])
    name = res["name"]
    desc = res["description"]
    params = res["params"]
    definition = res["source"]["definition"]
    body = res["source"]["body"]
    yields = res["source"]["yields"]
    metadata = {"name": name, "description": desc, "parameters": params}
    source = "\n".join([definition, body, yields])

    try:
        function = function_factory(source, metadata)
        yield Message(content=f"{function.__name__} created successfully.")
    except Exception as e:
        print(f"Error generating function: {e}")
        yield Message(content=f"Error generating function: {e}")


def function_factory(source, metadata):
    params = [f"{n}: {d['type']}" for n, d in metadata["parameters"].items()]
    header = f"async def {metadata['name']}({", ".join(params)}) -> SystemMessage:"
    assignment = f"    {metadata['name']}.metadata = {metadata}"
    body = f"    {source['body']}"
    yields = f"    yield SystemMessage(content={source['yields']})"

    try:
        full_function_code = "\n".join([header, assignment, body, yields])
        exec(full_function_code, globals())
    except Exception as e:
        print(f"Error building function: {e}")

    func = eval(metadata["name"])
    return func
