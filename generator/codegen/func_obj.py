from typing import Optional, Sequence
from codegen import func
from codegen.param_list import template


class CallableClass:
    def __init__(
        self,
        template_param_list: (
            template.TemplateTypeParamList
            | template.TemplateTypeArgumentList
            | None
        ),
        name: str,
        call_operators: Optional[Sequence[func.Function]],
        *,
        requires_clauses: Sequence[str] = tuple(),
    ) -> None:
        self.template_param_list: (
            template.TemplateTypeParamList
            | template.TemplateTypeArgumentList
            | None
        ) = template_param_list
        self.name: str = name
        if call_operators is not None:
            assert all(
                map(lambda op: op.func_name == "operator()", call_operators)
            )
        self.call_operators: Optional[Sequence[func.Function]] = call_operators
        self.requires_clauses: Sequence[str] = requires_clauses

    @property
    def cpp_repr(self) -> str:
        if isinstance(self.template_param_list, template.TemplateTypeParamList):
            template_clause = f"template {self.template_param_list.cpp_repr}\n"
        elif isinstance(
            self.template_param_list, template.TemplateTypeArgumentList
        ):
            template_clause = "template <>\n"
        else:
            template_clause = ""
        requires_clause = (
            ""
            if len(self.requires_clauses) == 0
            else "  requires " + " && ".join(self.requires_clauses) + "\n"
        )
        if isinstance(
            self.template_param_list, template.TemplateTypeArgumentList
        ):
            first_line = (
                f"struct {self.name}{self.template_param_list.cpp_repr}"
            )
        else:
            first_line = "struct " + self.name
        if self.call_operators is not None:
            operators = (
                " {\n"
                + "\n".join(map(lambda op: op.cpp_repr, self.call_operators))
                + "\n}"
            )
        else:
            operators = ""

        body = f"""namespace internal {{
{template_clause}{requires_clause}{first_line}{operators};
}}  // namespace internal"""

        if isinstance(self.template_param_list, template.TemplateTypeParamList):
            return f"""{body}
template {self.template_param_list.cpp_repr}
constexpr inline internal::{self.name}{self.template_param_list.forward.cpp_repr} {self.name}{{}};"""
        if isinstance(
            self.template_param_list, template.TemplateTypeArgumentList
        ):
            return body
        return f"""{body}
constexpr inline internal::{self.name} {self.name}{{}};"""
