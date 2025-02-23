from __future__ import annotations


class StateTransitionError(BaseException):
    pass


class RouterError(BaseException):
    pass


class ToolError(BaseException):
    pass


class ResourceError(BaseException):
    pass


class PromptError(BaseException):
    def __init__(self, prompt_id: str, message: str) -> None:
        super().__init__(
            dev_message=(
                (
                    f"Invalid prompt template: {prompt_id}. {message}. "
                    "This should not happen in production environment."
                )
            ),
            user_message=(
                (
                    "Sorry, scitus failed to generate a valid response for your request this time."
                )
            ),
            should_retry_later=False,
        )


class ContextUnavailable(BaseException):
    pass


class ContextNotFound(BaseException):
    pass
