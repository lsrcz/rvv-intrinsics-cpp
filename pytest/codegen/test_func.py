from typing import Optional
from codegen.param_list import function, template
from codegen import func, guarded
from codegen.type import misc, elem, vmask, vreg
import pytest


def test_apply_function_typed_param_list() -> None:
    assert (
        func.apply_function(
            "func",
            function.FunctionTypedParamList(
                function.TypedParam(type=misc.SizeTType(), name="param1"),
                function.TypedParam(
                    type=elem.FloatType(width=16), name="param2"
                ),
            ),
        )
        == "func(param1, param2)"
    )


def test_apply_function_argument_list() -> None:
    assert (
        func.apply_function(
            "func",
            function.FunctionArgumentList("param1", "param2"),
        )
        == "func(param1, param2)"
    )


def test_rv_postfix() -> None:
    assert func.rv_postfix("") == ""
    assert func.rv_postfix("m") == "_m"
    assert func.rv_postfix("tu") == "_tu"
    assert func.rv_postfix("tum") == "_tum"
    assert func.rv_postfix("mu") == "_mu"
    assert func.rv_postfix("tumu") == "_tumu"
    assert func.rv_postfix("", overloaded=True) == ""
    assert func.rv_postfix("m", overloaded=True) == ""
    assert func.rv_postfix("tu", overloaded=True) == "_tu"
    assert func.rv_postfix("tum", overloaded=True) == "_tum"
    assert func.rv_postfix("mu", overloaded=True) == "_mu"
    assert func.rv_postfix("tumu", overloaded=True) == "_tumu"


ret_type = elem.IntType(width=32, signed=True)
func_name = "func"
function_param_list = function.FunctionTypedParamList(
    function.TypedParam(type=elem.ParamElemType(typename="E"), name="param1"),
    function.TypedParam(type=elem.FloatType(width=16), name="param2"),
)
function_body = "  return 0;"
template_param_list = template.TemplateTypeParamList(
    elem.ParamElemType(typename="E")
)
single_require_clauses: list[str] = ["sizeof<E> == 4"]
multiple_require_clauses: list[str] = ["sizeof<E> == 4", "some_concept<E>"]
feature_guards: list[guarded.Guard] = guarded.elem_guard(
    elem.FloatType(width=16), need_zvfh=False
)


def test_function() -> None:
    function = func.Function(
        ret_type=ret_type,
        func_name=func_name,
        function_param_list=function_param_list,
        function_body=function_body,
        template_param_list=template_param_list,
        require_clauses=single_require_clauses,
        feature_guards=feature_guards,
    )
    assert (
        function.cpp_repr
        == """#if HAS_ZVFHMIN
template <typename E>
  requires sizeof<E> == 4
RVV_ALWAYS_INLINE
int32_t func(E param1, float16_t param2) {
  return 0;
}
#endif"""
    )


def test_function_no_body() -> None:
    function = func.Function(
        ret_type=ret_type,
        func_name=func_name,
        function_param_list=function_param_list,
        function_body=None,
        template_param_list=template_param_list,
        require_clauses=single_require_clauses,
        feature_guards=feature_guards,
    )
    assert (
        function.cpp_repr
        == """#if HAS_ZVFHMIN
template <typename E>
  requires sizeof<E> == 4
RVV_ALWAYS_INLINE
int32_t func(E param1, float16_t param2);
#endif"""
    )


def test_function_no_template() -> None:
    function = func.Function(
        ret_type=ret_type,
        func_name=func_name,
        function_param_list=function_param_list,
        function_body=function_body,
        feature_guards=feature_guards,
    )
    assert (
        function.cpp_repr
        == """#if HAS_ZVFHMIN
RVV_ALWAYS_INLINE
int32_t func(E param1, float16_t param2) {
  return 0;
}
#endif"""
    )


def test_function_template_no_requires() -> None:
    function = func.Function(
        ret_type=ret_type,
        func_name=func_name,
        function_param_list=function_param_list,
        function_body=function_body,
        template_param_list=template_param_list,
        feature_guards=feature_guards,
    )
    assert (
        function.cpp_repr
        == """#if HAS_ZVFHMIN
template <typename E>
RVV_ALWAYS_INLINE
int32_t func(E param1, float16_t param2) {
  return 0;
}
#endif"""
    )


def test_function_template_multiple_requires() -> None:
    function = func.Function(
        ret_type=ret_type,
        func_name=func_name,
        function_param_list=function_param_list,
        function_body=function_body,
        template_param_list=template_param_list,
        require_clauses=multiple_require_clauses,
        feature_guards=feature_guards,
    )
    assert (
        function.cpp_repr
        == """#if HAS_ZVFHMIN
template <typename E>
  requires sizeof<E> == 4 && some_concept<E>
RVV_ALWAYS_INLINE
int32_t func(E param1, float16_t param2) {
  return 0;
}
#endif"""
    )


def test_function_no_feature_guards() -> None:
    function = func.Function(
        ret_type=ret_type,
        func_name=func_name,
        function_param_list=function_param_list,
        function_body=function_body,
        template_param_list=template_param_list,
        require_clauses=single_require_clauses,
    )
    assert (
        function.cpp_repr
        == """template <typename E>
  requires sizeof<E> == 4
RVV_ALWAYS_INLINE
int32_t func(E param1, float16_t param2) {
  return 0;
}"""
    )


elem_type = elem.ParamElemType(typename="E")
ratio = misc.ParamSizeTValue(typename="kRatio")

base_param_list = function.FunctionTypedParamList(
    function.TypedParam(type=elem.ParamElemType(typename="E"), name="param1"),
    function.TypedParam(
        type=misc.ParamSizeTValue(typename="kRatio"), name="param2"
    ),
)

mask_extra = function.FunctionTypedParamList(
    function.TypedParam(type=vmask.VMaskType(ratio=ratio), name="vm")
)

dest_extra = function.FunctionTypedParamList(
    function.TypedParam(
        type=vreg.ConcreteVRegType(elem_type=elem_type, ratio=ratio), name="vd"
    )
)


@pytest.mark.parametrize(
    "variant,undisturbed_need_dest_arg,extra_list",
    [
        ("", False, function.FunctionTypedParamList()),
        ("", True, function.FunctionTypedParamList()),
        (
            "m",
            False,
            mask_extra,
        ),
        (
            "m",
            True,
            mask_extra,
        ),
        (
            "tu",
            False,
            function.FunctionTypedParamList(),
        ),
        (
            "tu",
            True,
            dest_extra,
        ),
        (
            "tu",
            None,
            dest_extra,
        ),
        (
            "tum",
            False,
            mask_extra,
        ),
        (
            "tum",
            True,
            mask_extra + dest_extra,
        ),
        (
            "mu",
            False,
            mask_extra,
        ),
        (
            "mu",
            True,
            mask_extra + dest_extra,
        ),
        (
            "tumu",
            False,
            mask_extra,
        ),
        (
            "tumu",
            True,
            mask_extra + dest_extra,
        ),
    ],
)
def test_elem_ratio_extend_param_list(
    variant: str,
    undisturbed_need_dest_arg: Optional[bool],
    extra_list: function.FunctionTypedParamList,
) -> None:
    if undisturbed_need_dest_arg is None:
        assert (
            func.elem_ratio_extend_param_list(
                elem_type=elem_type,
                ratio=ratio,
                variant=variant,
                param_list=base_param_list,
            )
            == extra_list + base_param_list
        )
    else:
        assert (
            func.elem_ratio_extend_param_list(
                elem_type=elem_type,
                ratio=ratio,
                variant=variant,
                param_list=base_param_list,
                undisturbed_need_dest_arg=undisturbed_need_dest_arg,
            )
            == extra_list + base_param_list
        )


vreg_type = vreg.ParamVRegType(typename="V")

vreg_base_param_list = function.FunctionTypedParamList(
    function.TypedParam(type=vreg_type, name="param1"),
    function.TypedParam(type=ratio, name="param2"),
)

vreg_dest_extra = function.FunctionTypedParamList(
    function.TypedParam(type=vreg_type, name="vd")
)


@pytest.mark.parametrize(
    "variant,undisturbed_need_dest_arg,extra_list",
    [
        ("", False, function.FunctionTypedParamList()),
        ("", True, function.FunctionTypedParamList()),
        (
            "m",
            False,
            mask_extra,
        ),
        (
            "m",
            True,
            mask_extra,
        ),
        (
            "tu",
            False,
            function.FunctionTypedParamList(),
        ),
        (
            "tu",
            True,
            vreg_dest_extra,
        ),
        (
            "tu",
            None,
            vreg_dest_extra,
        ),
        (
            "tum",
            False,
            mask_extra,
        ),
        (
            "tum",
            True,
            mask_extra + vreg_dest_extra,
        ),
        (
            "mu",
            False,
            mask_extra,
        ),
        (
            "mu",
            True,
            mask_extra + vreg_dest_extra,
        ),
        (
            "tumu",
            False,
            mask_extra,
        ),
        (
            "tumu",
            True,
            mask_extra + vreg_dest_extra,
        ),
    ],
)
def test_vreg_ratio_extend_param_list(
    variant: str,
    undisturbed_need_dest_arg: Optional[bool],
    extra_list: function.FunctionTypedParamList,
) -> None:
    if undisturbed_need_dest_arg is None:
        assert (
            func.vreg_ratio_extend_param_list(
                vreg_type=vreg_type,
                ratio=ratio,
                variant=variant,
                param_list=base_param_list,
            )
            == extra_list + base_param_list
        )
    else:
        assert (
            func.vreg_ratio_extend_param_list(
                vreg_type=vreg_type,
                ratio=ratio,
                variant=variant,
                param_list=base_param_list,
                undisturbed_need_dest_arg=undisturbed_need_dest_arg,
            )
            == extra_list + base_param_list
        )
