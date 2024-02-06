from typing import Callable, Optional, Sequence
from codegen.param_list import function, template
from codegen import guarded, constraints, validate
from codegen.type import type, misc, elem, vmask, vreg


def apply_function(
    func: str,
    param_list: function.FunctionTypedParamList | function.FunctionArgumentList,
) -> str:
    if isinstance(param_list, function.FunctionTypedParamList):
        return apply_function(func, param_list.forward)
    return f"{func}{param_list.cpp_repr}"


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
            f"{cpp_intrinsics_base_name}",
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


def for_all_elem_ratio(
    ret_type: Callable[[elem.RawElemType, misc.LitSizeTValue], type.Type],
    cpp_intrinsics_base_name: str,
    function_param_list: Callable[
        [str, elem.RawElemType, misc.LitSizeTValue],
        function.FunctionTypedParamList,
    ],
    function_body: Callable[
        [
            str,
            elem.RawElemType,
            misc.LitSizeTValue,
            function.FunctionTypedParamList,
        ],
        Optional[str],
    ],
    *,
    need_zvfh: bool = True,
    template_param_list: Optional[template.TemplateTypeParamList] = None,
    require_clauses: Sequence[str] = tuple(),
    feature_guards: Optional[
        Callable[
            [elem.RawElemType, misc.LitSizeTValue], Sequence[guarded.Guard]
        ]
    ] = None,
) -> Callable[[str, elem.RawElemType, misc.LitSizeTValue], Optional[Function]]:
    if feature_guards is None:
        feature_guards = lambda elem_type, ratio: guarded.elem_ratio_guard(
            elem_type, ratio, need_zvfh
        )

    def inner(
        variant: str, elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
    ) -> Optional[Function]:
        if not validate.is_compatible_elem_ratio_may_under_guards(
            elem_type, ratio
        ):
            return None
        param_list = function_param_list(variant, elem_type, ratio)
        return Function(
            ret_type(elem_type, ratio),
            f"{cpp_intrinsics_base_name}{rv_postfix(variant)}",
            param_list,
            function_body(variant, elem_type, ratio, param_list),
            template_param_list=template_param_list,
            require_clauses=require_clauses,
            feature_guards=feature_guards(elem_type, ratio),
        )

    return inner


def elem_ratio_extend_param_list(
    elem_type: elem.ElemType,
    ratio: misc.SizeTValue,
    variant: str,
    param_list: function.FunctionTypedParamList,
    undisturbed_need_dest_arg: bool = True,
) -> function.FunctionTypedParamList:
    return (
        function.FunctionTypedParamList(
            *(
                [
                    function.TypedParam(
                        type=vmask.VMaskType(ratio=ratio), name="vm"
                    )
                ]
                if "m" in variant
                else []
            )
            + (
                [
                    function.TypedParam(
                        type=vreg.ConcreteVRegType(
                            elem_type=elem_type, ratio=ratio
                        ),
                        name="vd",
                    )
                ]
                if variant not in ["", "m"] and undisturbed_need_dest_arg
                else []
            )
        )
        + param_list
    )


def template_elem_ratio_for_all_size(
    ret_type: Callable[[elem.ParamElemType, misc.ParamSizeTValue], type.Type],
    cpp_intrinsics_base_name: str,
    function_param_list: Callable[
        [str, elem.ParamElemType, misc.ParamSizeTValue, int],
        function.FunctionTypedParamList,
    ],
    function_body: Callable[
        [
            str,
            elem.ParamElemType,
            misc.ParamSizeTValue,
            int,
            function.FunctionTypedParamList,
        ],
        Optional[str],
    ],
    *,
    template_param_list: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue],
        Optional[template.TemplateTypeParamList],
    ] = lambda elem_type, ratio: template.TemplateTypeParamList(
        elem_type, ratio
    ),
    require_clauses: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue, int], Sequence[str]
    ] = lambda elem_type, ratio, width: [
        constraints.has_width(elem_type, width),
        constraints.is_compatible_elem_ratio(elem_type, ratio),
    ],
    feature_guards: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue], Sequence[guarded.Guard]
    ] = lambda elem_type, ratio: tuple(),
) -> Callable[[str, int], Optional[Function]]:
    elem_type = elem.ParamElemType(typename="E")
    ratio = misc.ParamSizeTValue(typename="kRatio")

    def inner(variant: str, width: int) -> Optional[Function]:
        param_list = function_param_list(variant, elem_type, ratio, width)
        return Function(
            ret_type(elem_type, ratio),
            f"{cpp_intrinsics_base_name}",
            param_list,
            function_body(variant, elem_type, ratio, width, param_list),
            template_param_list=template_param_list(elem_type, ratio),
            require_clauses=require_clauses(elem_type, ratio, width),
            feature_guards=feature_guards(elem_type, ratio),
        )

    return inner


def template_elem_ratio(
    ret_type: Callable[[elem.ParamElemType, misc.ParamSizeTValue], type.Type],
    cpp_intrinsics_base_name: str,
    function_param_list: Callable[
        [str, elem.ParamElemType, misc.ParamSizeTValue],
        function.FunctionTypedParamList,
    ],
    function_body: Callable[
        [
            str,
            elem.ParamElemType,
            misc.ParamSizeTValue,
            function.FunctionTypedParamList,
        ],
        Optional[str],
    ],
    *,
    template_param_list: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue],
        Optional[template.TemplateTypeParamList],
    ] = lambda elem_type, ratio: template.TemplateTypeParamList(
        elem_type, ratio
    ),
    require_clauses: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue], Sequence[str]
    ] = lambda elem_type, ratio: [
        constraints.is_compatible_elem_ratio(elem_type, ratio),
    ],
    feature_guards: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue], Sequence[guarded.Guard]
    ] = lambda _, __: tuple(),
) -> Callable[[str], Function]:
    elem_type = elem.ParamElemType(typename="E")
    ratio = misc.ParamSizeTValue(typename="kRatio")

    def inner(variant: str) -> Function:
        param_list = function_param_list(variant, elem_type, ratio)
        return Function(
            ret_type(elem_type, ratio),
            f"{cpp_intrinsics_base_name}",
            param_list,
            function_body(variant, elem_type, ratio, param_list),
            template_param_list=template_param_list(elem_type, ratio),
            require_clauses=require_clauses(elem_type, ratio),
            feature_guards=feature_guards(elem_type, ratio),
        )

    return inner


def vreg_ratio_extend_param_list(
    vreg_type: vreg.VRegType,
    ratio: misc.SizeTValue,
    variant: str,
    param_list: function.FunctionTypedParamList,
    undisturbed_need_dest_arg: bool = True,
) -> function.FunctionTypedParamList:
    return (
        function.FunctionTypedParamList(
            *(
                [
                    function.TypedParam(
                        type=vmask.VMaskType(ratio=ratio), name="vm"
                    )
                ]
                if "m" in variant
                else []
            )
            + (
                [
                    function.TypedParam(
                        type=vreg_type,
                        name="vd",
                    )
                ]
                if variant not in ["", "m"] and undisturbed_need_dest_arg
                else []
            )
        )
        + param_list
    )


def template_vreg_ratio(
    ret_type: Callable[[vreg.ParamVRegType, misc.ParamSizeTValue], type.Type],
    cpp_intrinsics_base_name: str,
    function_param_list: Callable[
        [str, vreg.ParamVRegType, misc.ParamSizeTValue],
        function.FunctionTypedParamList,
    ],
    function_body: Callable[
        [
            str,
            vreg.ParamVRegType,
            misc.ParamSizeTValue,
            function.FunctionTypedParamList,
        ],
        Optional[str],
    ],
    *,
    template_param_list: Callable[
        [vreg.ParamVRegType, misc.ParamSizeTValue],
        Optional[template.TemplateTypeParamList],
    ] = lambda vreg_type, ratio: template.TemplateTypeParamList(
        vreg_type, ratio
    ),
    require_clauses: Callable[
        [vreg.ParamVRegType, misc.ParamSizeTValue], Sequence[str]
    ] = lambda vreg_type, ratio: [
        constraints.is_compatible_vreg_ratio(vreg_type, ratio),
    ],
    feature_guards: Callable[
        [vreg.ParamVRegType, misc.ParamSizeTValue], Sequence[guarded.Guard]
    ] = lambda _, __: tuple(),
) -> Callable[[str], Function]:
    vreg_type = vreg.ParamVRegType(typename="V")
    ratio = misc.ParamSizeTValue(typename="kRatio")

    def inner(variant: str) -> Function:
        param_list = function_param_list(variant, vreg_type, ratio)
        return Function(
            ret_type(vreg_type, ratio),
            f"{cpp_intrinsics_base_name}",
            param_list,
            function_body(variant, vreg_type, ratio, param_list),
            template_param_list=template_param_list(vreg_type, ratio),
            require_clauses=require_clauses(vreg_type, ratio),
            feature_guards=feature_guards(vreg_type, ratio),
        )

    return inner
