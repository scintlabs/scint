from __future__ import annotations


class StateTransitionError(Exception):
    pass


class RouterError(Exception):
    pass


class ToolError(Exception):
    pass


class ResourceError(Exception):
    pass


class PromptError(Exception):
    pass


class ContextUnavailable(BaseException):
    pass


class ContextNotFound(BaseException):
    pass
