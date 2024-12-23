from src.network.models import Block, Instruction


critique = Instruction(
    name="critique",
    description="Generate critiques.",
    labels=[],
    content=[
        Block(
            content="You are a critiquing algorithm. For every message, point out the flaws in logic, poor reasoning, bad ideas, sloppy components, and any other issue you can find with the presented topic."
        )
    ],
)

rebuttal = Instruction(
    name="rebuttal",
    description="Generate critique rebuttals.",
    labels=[],
    content=[
        Block(
            content="You are a rebuttal algorithm. For every critique, criticism, apparent flaw, or doubt, produce an elegant and creative solution."
        )
    ],
)

build_func_blocks = Block(
    content="""
    You're responsible for generating metadata annotations, defined with the JSON schema below. For every message containing intent src code, use the schema to describe the intent thoroughly, including descriptions and type annotations for each parameter. If annotations are missing from the intent signature, infer them from the intent body. Be sure to return valid JSON format.

    The schema:

    {
        "description": "A description of the intent.",
        "parameters": {
            "type": "object",
            "properties": {
                "string_param_name": {
                    "type": "string",
                    "description": "Some description.",
                },
                "integer_param_name": {
                    "type": "integer",
                    "description": "Some description.",
                },
                "boolean_param_name": {
                    "type": "boolean",
                    "description": "A boolean parameter.",
                },
                "enum_param_name": {
                    "type": "string",
                    "description": "Strings with enums are used to restrict parameters.",
                    "enum": ["enum", "list", "of", "options"],
                },
                "object_param_name": {
                    "type": "object",
                    "description": "Nested components follow the same schema as above.",
                    "properties": {
                        "string_param_name": {
                            "type": "string",
                            "description": "Some description.",
                        },
                    },
                },
            },
            "required": ["all", "required", "params"],
        },
    }
    """
)
