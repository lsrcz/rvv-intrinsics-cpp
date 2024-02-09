from typing import Sequence
from codegen import func
from codegen.param_list import template


class CallableClass:
    def __init__(
        self,
        template_param_list: template.TemplateTypeParamList,
        name: str,
        call_operators: Sequence[func.Function],
        *,
        requires_clauses: Sequence[str] = tuple(),
    ) -> None:
        self.template_param_list: template.TemplateTypeParamList = (
            template_param_list
        )
        self.name: str = name
        assert len(template_param_list) > 0
        assert len(call_operators) > 0
        assert all(map(lambda op: op.func_name == "operator()", call_operators))
        self.call_operators: Sequence[func.Function] = call_operators
        self.requires_clauses: Sequence[str] = requires_clauses

    @property
    def cpp_repr(self) -> str:
        template_clause = f"template {self.template_param_list.cpp_repr}\n"
        requires_clause = (
            ""
            if len(self.requires_clauses) == 0
            else "  requires " + " && ".join(self.requires_clauses) + "\n"
        )
        first_line = "struct " + self.name + " {\n"
        operators = "\n".join(map(lambda op: op.cpp_repr, self.call_operators))
        last_line = "};"

        return f"""namespace internal {{
{template_clause}{requires_clause}{first_line}{operators}
{last_line}
}}  // namespace internal
template {self.template_param_list.cpp_repr}
constexpr inline internal::{self.name}{self.template_param_list.forward.cpp_repr} {self.name}{{}};"""
