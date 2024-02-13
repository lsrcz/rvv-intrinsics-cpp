from typing import Callable, Optional, Sequence

from codegen import constraints, guarded, validate
from codegen.param_list import function, template
from codegen.typing import base, elem, misc, vmask, vreg


def apply_function(
    func: str,
    param_list: function.FunctionTypedParamList | function.FunctionArgumentList,
) -> str:
    if isinstance(param_list, function.FunctionTypedParamList):
        return apply_function(func, param_list.forward)
    return f"{func}{param_list.cpp_repr}"


def rvv_postfix(variant: str, overloaded: bool = False) -> str:
    if variant == "":
        return ""
    if variant == "m" and overloaded:
        return ""
    else:
        return f"_{variant}"


class Function:
    def __init__(
        self,
        ret_type: base.Type,
        func_name: str,
        function_param_list: function.FunctionTypedParamList,
        function_body: Optional[str],
        *,
        template_param_list: Optional[template.TemplateTypeParamList] = None,
        require_clauses: Sequence[str] = tuple(),
        feature_guards: Sequence[guarded.Guard] = tuple(),
        modifier: str = "",
    ) -> None:
        if not template_param_list:
            assert len(require_clauses) == 0
        self.template_param_list: Optional[template.TemplateTypeParamList] = (
            template_param_list
        )
        self.require_clauses: Sequence[str] = require_clauses
        self.ret_type: base.Type = ret_type
        self.func_name: str = func_name
        self.function_param_list: function.FunctionTypedParamList = (
            function_param_list
        )
        self.modifier = modifier
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
{self.ret_type.cpp_repr} {self.func_name}{self.function_param_list.cpp_repr}"""
        modifier = "" if self.modifier == "" else f" {self.modifier}"
        body_or_semicolon: str = (
            f" {{\n{self.function_body}\n}}" if self.function_body else ";"
        )
        string: str = (
            template_clause
            + requires_clause
            + declaration
            + modifier
            + body_or_semicolon
        )
        return guarded.Guarded(self.feature_guards, string).cpp_repr


def template_ratio(
    ret_type: Callable[[misc.ParamSizeTValue], base.Type],
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
    ] = template.TemplateTypeParamList,
    require_clauses: Callable[
        [misc.ParamSizeTValue], Sequence[str]
    ] = lambda ratio: [constraints.supported_ratio(ratio)],
    feature_guards: Callable[
        [misc.ParamSizeTValue], Sequence[guarded.Guard]
    ] = lambda ratio: tuple(),
) -> Callable[[str], Function]:
    def inner(variant: str) -> Function:
        ratio = misc.param_size_t("kRatio")
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
    ret_type: Callable[[misc.LitSizeTValue], base.Type],
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
    ] = guarded.ratio_guard,
    modifier: str = "",
) -> Callable[[str, misc.LitSizeTValue], Function]:
    def inner(variant: str, ratio: misc.LitSizeTValue) -> Function:
        param_list = function_param_list(variant, ratio)
        return Function(
            ret_type(ratio),
            f"{cpp_intrinsics_base_name}",
            param_list,
            function_body(variant, ratio, param_list),
            template_param_list=template_param_list,
            require_clauses=require_clauses,
            feature_guards=feature_guards(ratio),
            modifier=modifier,
        )

    return inner


def for_all_elem_ratio(
    ret_type: Callable[[elem.RawElemType, misc.LitSizeTValue], base.Type],
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
    def final_feature_guards(
        elem_type: elem.RawElemType, ratio: misc.LitSizeTValue
    ):
        if feature_guards is not None:
            return feature_guards(elem_type, ratio)
        return guarded.elem_ratio_guard(elem_type, ratio, need_zvfh)

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
            f"{cpp_intrinsics_base_name}",
            param_list,
            function_body(variant, elem_type, ratio, param_list),
            template_param_list=template_param_list,
            require_clauses=require_clauses,
            feature_guards=final_feature_guards(elem_type, ratio),
        )

    return inner


def elem_ratio_extend_param_list(
    elem_type: elem.ElemType,
    ratio: misc.SizeTValue,
    variant: str,
    param_list: function.FunctionTypedParamList,
    undisturbed_need_dest_arg: bool = True,
    comparing: bool = False,
) -> function.FunctionTypedParamList:
    extended_param_list = function.param_list()
    if "m" in variant:
        extended_param_list = extended_param_list + (
            vmask.concrete(ratio=ratio),
            "vm",
        )
    if variant not in ["", "m"] and undisturbed_need_dest_arg:
        extended_param_list = extended_param_list + (
            (
                vmask.concrete(ratio=ratio)
                if comparing
                else vreg.concrete(elem_type, ratio)
            ),
            "vd",
        )
    return extended_param_list + param_list


def elem_ratio_param_list(
    elem_type: elem.ElemType,
    ratio: misc.SizeTValue,
    variant: str,
    type_list: Sequence[base.Type],
    name_list: Sequence[str],
    undisturbed_need_dest_arg: bool = True,
    comparing: bool = False,
) -> function.FunctionTypedParamList:
    return elem_ratio_extend_param_list(
        elem_type,
        ratio,
        variant,
        function.param_list(type_list, name_list),
        undisturbed_need_dest_arg,
        comparing,
    )


def template_elem_ratio_for_all_size(
    ret_type: Callable[[elem.ParamElemType, misc.ParamSizeTValue], base.Type],
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
    ] = template.TemplateTypeParamList,
    require_clauses: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue, int], Sequence[str]
    ] = lambda elem_type, ratio, width: [
        constraints.has_width(elem_type, width),
        constraints.compatible_elem_ratio(elem_type, ratio),
    ],
    feature_guards: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue], Sequence[guarded.Guard]
    ] = lambda elem_type, ratio: tuple(),
) -> Callable[[str, int], Optional[Function]]:
    elem_type = elem.param("E")
    ratio = misc.param_size_t("kRatio")

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
    ret_type: Callable[[elem.ParamElemType, misc.ParamSizeTValue], base.Type],
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
    ] = template.TemplateTypeParamList,
    require_clauses: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue], Sequence[str]
    ] = lambda elem_type, ratio: [
        constraints.compatible_elem_ratio(elem_type, ratio),
    ],
    feature_guards: Callable[
        [elem.ParamElemType, misc.ParamSizeTValue], Sequence[guarded.Guard]
    ] = lambda _, __: tuple(),
) -> Callable[[str], Function]:
    elem_type = elem.param("E")
    ratio = misc.param_size_t("kRatio")

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
    dest_type: base.Type,
    ratio: misc.SizeTValue,
    variant: str,
    param_list: function.FunctionTypedParamList,
    undisturbed_need_dest_arg: bool = True,
) -> function.FunctionTypedParamList:
    extended_param_list = function.param_list()
    if "m" in variant:
        extended_param_list = extended_param_list + (
            vmask.concrete(ratio=ratio),
            "vm",
        )
    if variant not in ["", "m"] and undisturbed_need_dest_arg:
        extended_param_list = extended_param_list + (
            dest_type,
            "vd",
        )
    return extended_param_list + param_list


def vreg_ratio_param_list(
    dest_type: base.Type,
    ratio: misc.SizeTValue,
    variant: str,
    type_list: Sequence[base.Type],
    name_list: Sequence[str],
    undisturbed_need_dest_arg: bool = True,
) -> function.FunctionTypedParamList:
    return vreg_ratio_extend_param_list(
        dest_type,
        ratio,
        variant,
        function.param_list(type_list, name_list),
        undisturbed_need_dest_arg,
    )


def template_vreg_ratio(
    ret_type: Callable[[vreg.ParamVRegType, misc.ParamSizeTValue], base.Type],
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
    ] = template.TemplateTypeParamList,
    require_clauses: Callable[
        [vreg.ParamVRegType, misc.ParamSizeTValue], Sequence[str]
    ] = lambda vreg_type, ratio: [
        constraints.compatible_vreg_ratio(vreg_type, ratio),
    ],
    feature_guards: Callable[
        [vreg.ParamVRegType, misc.ParamSizeTValue], Sequence[guarded.Guard]
    ] = lambda _, __: tuple(),
    modifier: str = "",
) -> Callable[[str], Function]:
    vreg_type = vreg.param("V")
    ratio = misc.param_size_t("kRatio")

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
            modifier=modifier,
        )

    return inner
