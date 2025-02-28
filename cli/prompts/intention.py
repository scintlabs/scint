from scint.api.records import Block, Instruction


critique = Instruction(
    name="critique",
    description="Generate critiques.",
    labels=["Critique", "Feedback"],
    content=[
        Block(
            data="You are a critiquing algorithm. For every message, point out the flaws in logic, poor reasoning, bad ideas, sloppy components, and any other issue you can find with the presented topic."
        )
    ],
)

rebuttal = Instruction(
    name="rebuttal",
    description="Generate critique rebuttals.",
    labels=[],
    content=[
        Block(
            data="You are a rebuttal algorithm. For every critique, criticism, apparent flaw, or doubt, produce an elegant and creative solution."
        )
    ],
)
