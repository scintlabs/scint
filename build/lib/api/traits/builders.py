from __future__ import annotations

import ast
from typing import Any, Type

from scint.api.models import Specification
from scint.api.records import Argument, Arguments
from scint.api.types import Struct, Trait


class ClassBuilder(Trait):
    def build_class(self, spec) -> Type:
        def class_def(self, spec: Specification):
            def arguments(spec): ...

            def body(spec):
                body = []
                if spec.docstring:
                    body.insert(0, ast.Expr(value=ast.Constant(value=spec.docstring)))

                for method_spec in spec.methods or []:
                    method_builder = Builder()
                    method_node = method_builder.select_spec(method_spec)
                    body.append(method_node)

                for attr, value in (spec.attributes or {}).items():
                    body.append(
                        ast.Assign(
                            targets=[ast.Name(id=attr, ctx=ast.Store())],
                            value=ast.Constant(value=value),
                        )
                    )
                return body

            def methods(spec): ...

            return ast.ClassDef(
                name=spec.name,
                bases=[
                    ast.Name(id=base, ctx=ast.Load()) for base in (spec.typess or [])
                ],
                keywords=[],
                body=body,
                decorator_list=[],
            )

        module = ast.Module(body=[class_def], type_ignores=[])
        ast.fix_missing_locations(module)
        code = compile(module, "<ast>", "exec")
        namespace = {}
        exec(code, namespace)
        return namespace[spec.name]


class FunctionBuilder(Trait):
    def build_func(self, spec) -> ast.FunctionType:
        def func_def(self, spec: Specification):
            def arguments(spec):
                args_list = []
                for arg in spec.args:
                    annotation = spec.annotations.get(arg, None)
                    arg_node = ast.arg(
                        arg=arg,
                        annotation=(
                            ast.Name(id=annotation, ctx=ast.Load())
                            if annotation
                            else None
                        ),
                    )
                    args_list.append(arg_node)

                return ast.arguments(
                    posonlyargs=[],
                    args=args_list,
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[ast.Constant(value=d) for d in spec.defaults],
                )

            def body(spec):
                body = []

                if spec.docstring:
                    body.append(ast.Expr(ast.Constant(value=spec.docstring)))

                for line in spec.body:
                    line_ast = ast.parse(line).body
                    body.extend(line_ast)

                return body

            return ast.FunctionDef(
                name=spec.name,
                args=lambda spec: arguments(spec),
                body=lambda spec: body(spec),
                decorator_list=[
                    ast.Name(id=d, ctx=ast.Load()) for d in spec.decorators
                ],
                returns=None,
            )

        module = ast.Module(body=[lambda spec: func_def(spec)], type_ignores=[])
        ast.fix_missing_locations(module)
        code = compile(module, "<ast>", "exec")
        namespace = {}
        exec(code, namespace)
        return namespace[spec.name]


class ArgBuilder(Trait):
    def add_arg(self, name: str, type_: str, value: Any = None, req: bool = False):
        self._args.append(Argument(name=name, type=type_, value=value, required=req))
        return self

    def add_kwarg(self, name: str, type_: str, value: Any = None, req: bool = False):
        self._kwargs[name] = Argument(name=name, type=type_, value=value, required=req)
        return self

    def build(self):
        return Arguments(args=self._args, kwargs=self._kwargs)

    def model(self):
        pass


class ModelBuilder: ...


class Builder(Struct): ...
