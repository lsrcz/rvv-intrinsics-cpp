from typing import Callable, Optional, Sequence
from codegen.param_list import function, template
from codegen import guarded, constraints
from codegen.type import type, misc


def apply_function(
    func: str,
    param_list: function.FunctionTypedParamList | function.FunctionArgumentList,
) -> str:
    if isinstance(param_list, function.FunctionTypedParamList):
        return apply_function(func, param_list.forward)
    return f"{func}{param_list.cpp_repr}"


def cpp_postfix(variant: str) -> str:
    match variant:
        case "" | "m":
            return ""
        case "tu" | "tum":
            return "_tu"
        case _:
            return f"_{variant}"


def rv_postfix(variant: str, overloaded: bool = False) -> str:
    if variant == "":
        return ""
    if variant == "m" and overloaded:
        return ""
    else:
        return f"_{variant}"


class Function:
    def __init__(
        self,
        ret_type: type.Type,
        func_name: str,
        function_param_list: function.FunctionTypedParamList,
        function_body: Optional[str],
        *,
        template_param_list: Optional[template.TemplateTypeParamList] = None,
        require_clauses: Sequence[str] = tuple(),
        feature_guards: Sequence[guarded.Guard] = tuple(),
    ) -> None:
        if not template_param_list:
            assert len(require_clauses) == 0
        self.template_param_list: Optional[template.TemplateTypeParamList] = (
            template_param_list
        )
        self.require_clauses: Sequence[str] = require_clauses
        self.ret_type: type.Type = ret_type
        self.cpp_intrinsics_base_name: str = func_name
        self.function_param_list: function.FunctionTypedParamList = (
            function_param_list
        )
        self.function_body: Optional[str] = function_body
        self.feature_guards: Sequence[guarded.Guard] = feature_guards

    @property
    def cpp_repr(self) -> str:
        template_clause: str = (
            f"template {self.template_param_list.cpp_repr}\n"
            if self.template_param_list is not None
            else ""
        )
        requires_clause: str = (
            ""
            if len(self.require_clauses) == 0
            else "  requires " + " && ".join(self.require_clauses) + "\n"
        )
        declaration: str = f"""RVV_ALWAYS_INLINE
{self.ret_type.cpp_repr} {self.cpp_intrinsics_base_name}{self.function_param_list.cpp_repr}"""
        body_or_semicolon: str = (
            f" {{\n{self.function_body}\n}}" if self.function_body else ";"
        )
        string: str = (
            template_clause + requires_clause + declaration + body_or_semicolon
        )
        return guarded.Guarded(self.feature_guards, string).cpp_repr


def template_ratio(
    ret_type: Callable[[misc.ParamSizeTValue], type.Type],
    cpp_intrinsics_base_name: str,
    function_param_list: Callable[
        [str, misc.ParamSizeTValue], function.FunctionTypedParamList
    ],
    function_body: Callable[
        [str, misc.ParamSizeTValue, function.FunctionTypedParamList],
        Optional[str],
    ],
    *,
    template_param_list: Callable[
        [misc.ParamSizeTValue], Optional[template.TemplateTypeParamList]
    ] = lambda ratio: template.TemplateTypeParamList(ratio),
    require_clauses: Callable[
        [misc.ParamSizeTValue], Sequence[str]
    ] = lambda ratio: [constraints.is_supported_ratio(ratio)],
    feature_guards: Callable[
        [misc.ParamSizeTValue], Sequence[guarded.Guard]
    ] = lambda ratio: tuple(),
) -> Callable[[str], Function]:
    def inner(variant: str) -> Function:
        ratio = misc.ParamSizeTValue(typename="kRatio")
        param_list = function_param_list(variant, ratio)
        return Function(
            ret_type(ratio),
            f"{cpp_intrinsics_base_name}{cpp_postfix(variant)}",
            param_list,
            function_body(variant, ratio, param_list),
            template_param_list=template_param_list(ratio),
            require_clauses=require_clauses(ratio),
            feature_guards=feature_guards(ratio),
        )

    return inner


def for_all_ratio(
    ret_type: Callable[[misc.LitSizeTValue], type.Type],
    cpp_intrinsics_base_name: str,
    function_param_list: Callable[
        [str, misc.LitSizeTValue], function.FunctionTypedParamList
    ],
    function_body: Callable[
        [str, misc.LitSizeTValue, function.FunctionTypedParamList],
        Optional[str],
    ],
    *,
    template_param_list: Optional[template.TemplateTypeParamList] = None,
    require_clauses: Sequence[str] = tuple(),
    feature_guards: Callable[
        [misc.LitSizeTValue], Sequence[guarded.Guard]
    ] = lambda ratio: guarded.ratio_guard(ratio),
) -> Callable[[str, misc.LitSizeTValue], Function]:
    def inner(variant: str, ratio: misc.LitSizeTValue) -> Function:
        param_list = function_param_list(variant, ratio)
        return Function(
            ret_type(ratio),
            f"{cpp_intrinsics_base_name}{rv_postfix(variant)}",
            param_list,
            function_body(variant, ratio, param_list),
            template_param_list=template_param_list,
            require_clauses=require_clauses,
            feature_guards=feature_guards(ratio),
        )

    return inner
