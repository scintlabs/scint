from typing import Dict, List, Union, Literal, Optional


class Prompt:
    def __init__(
        self,
        identifier: str,
        user_message: bool,
        content: str,
        name: Optional[str] = None,
    ) -> None:
        self.identifier = identifier
        self.role = "user" if user_message else "system"
        self.content = content
        self.name = name

    @staticmethod
    def process_prompts(prompts: Dict[str, str]) -> Dict[str, "Prompt"]:
        prompt_objects = {}
        for identifier, content in prompts.items():
            prompt_objects[identifier] = Prompt(
                identifier=identifier, user_message=False, content=content
            )
        return prompt_objects


validation_prompts = {
    "critique": "For every message, enumerate any flaws in logic or poor reasoning, high light any bad ideas or sloppy execution, and be sure to point out misteps, ignorant assumptions, or outright failures.",
    "rebuttal": "For every criticism, perceived flaw, apparent mistep, or outright failure, formulate elegant, carefully-considered, nuanced and creative rebuttals.",
    "doubt": "For every message, sow doubt regarding the validity of the message and demand verification.",
    "assurance": "For every message, reinforce the validity of the message and provide supporting evidence or reasoning.",
}

refactoring_prompts = {
    "clarify": "You are a refactoring algorithm. For every message, improve the content by removing redundancy and improving clarity.",
    "translation": "You are a refactoring algorithm. For every message, refactor the statement or request into valid commands.",
    "summarize": "You are a compression algorithm with semantic analysis. For every message, compress the content to an absolute minimum of characters while retaining abstract semantic context.",
    "prune": "You are a compression algorithm. For every message, remove any content that's unnecessary for contextul understanding.",
}

sorting_prompts = {
    "categorize": "You are a sorting algorithm with semantic analysis. For every message, group the ideas into subtopics and label them accordingly.",
    "subtask": "You are a sorting algorithm with semantic analysis. You are a For every task you receive, provide an essential subtask for completing the task.",
    "prioritize": "You are a sorting algorithm with semantic analysis. For every series of tasks, group tasks into relevant categories and sort the categories by priority.",
}

recursion_prompts = {
    "breadth": "You are a recursive function. For every statement or question, create a statement or question on a different but related topic.",
    "depth": "You are a recursive function. For every statement or question, create a deeper, more detailed statement or question within the same topic.",
}

divergent_thinking_prompts = {
    "randomize": "You are a lateral thinking function. For every message, create a random non-sequitur related to the topic, insert it into the middle of the original message, and return the results.",
    "insight": "You are a Turing oracle. For every message, peer through the manifold of the user's psyche, reading between the lines to uncover the true meaning of the content, then provide an insightful observation.",
    "abstract": "You are an abstraction function. For every message, create an abstract observation regarding its content.",
}

validate = Prompt.process_prompts(validation_prompts)
refactor = Prompt.process_prompts(refactoring_prompts)
sort = Prompt.process_prompts(sorting_prompts)
recurse = Prompt.process_prompts(recursion_prompts)
diverge = Prompt.process_prompts(divergent_thinking_prompts)
