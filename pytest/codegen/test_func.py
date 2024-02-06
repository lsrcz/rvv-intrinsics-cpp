from codegen.param_list import function, template
from codegen import func, guarded
from codegen.type import misc, elem


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
