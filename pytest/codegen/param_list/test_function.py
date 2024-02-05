import pytest
from codegen.type import elem
from codegen.param_list import function

arg0 = function.TypedParam(type=elem.FloatType(width=32), name="arg0")
arg1 = function.TypedParam(type=elem.FloatType(width=64), name="arg1")
arg2 = function.TypedParam(type=elem.FloatType(width=16), name="arg2")

param_list_empty = function.FunctionTypedParamList()
param_list_0 = function.FunctionTypedParamList(arg0)
param_list_1 = function.FunctionTypedParamList(arg1)
param_list_01 = function.FunctionTypedParamList(arg0, arg1)
param_list_012 = function.FunctionTypedParamList(arg0, arg1, arg2)
param_list_12 = function.FunctionTypedParamList(arg1, arg2)

arg_list_empty = function.FunctionArgumentList()
arg_list_0 = function.FunctionArgumentList("arg0")
arg_list_1 = function.FunctionArgumentList("arg1")
arg_list_01 = function.FunctionArgumentList("arg0", "arg1")
arg_list_012 = function.FunctionArgumentList("arg0", "arg1", "arg2")
arg_list_12 = function.FunctionArgumentList("arg1", "arg2")


def test_typed_param() -> None:
    assert param_list_0.cpp_repr == "(float32_t arg0)"


@pytest.mark.parametrize(
    "function_param_list,expected",
    [
        (
            param_list_empty,
            "()",
        ),
        (
            param_list_0,
            "(float32_t arg0)",
        ),
        (
            param_list_01,
            "(float32_t arg0, float64_t arg1)",
        ),
    ],
)
def test_function_typed_param_list_cpp_repr(
    function_param_list: function.FunctionTypedParamList, expected: str
) -> None:
    assert function_param_list.cpp_repr == expected


def test_function_typed_param_list_forward() -> None:
    assert param_list_01.forward == arg_list_01


def test_function_typed_param_list_add() -> None:
    assert (param_list_0 + param_list_1) == param_list_01


def test_function_typed_param_list_len() -> None:
    assert len(param_list_01) == 2


def test_function_typed_param_list_get_single_item() -> None:
    assert param_list_012[0] == arg0
    assert param_list_012[1] == arg1
    assert param_list_012[2] == arg2


def test_function_typed_param_list_get_slice() -> None:
    assert param_list_012[0:2] == param_list_01
    assert param_list_012[0:3] == param_list_012
    assert param_list_012[1:3] == param_list_12


@pytest.mark.parametrize(
    "function_arg_list,expected",
    [
        (
            arg_list_empty,
            "()",
        ),
        (
            arg_list_0,
            "(arg0)",
        ),
        (
            arg_list_01,
            "(arg0, arg1)",
        ),
    ],
)
def test_function_typed_arg_list_cpp_repr(
    function_arg_list: function.FunctionArgumentList, expected: str
) -> None:
    assert function_arg_list.cpp_repr == expected


def test_function_typed_arg_list_add() -> None:
    assert (arg_list_0 + arg_list_1) == arg_list_01


def test_function_typed_arg_list_len() -> None:
    assert len(arg_list_01) == 2


def test_function_typed_arg_list_get_single_item() -> None:
    assert arg_list_012[0] == "arg0"
    assert arg_list_012[1] == "arg1"
    assert arg_list_012[2] == "arg2"


def test_function_typed_arg_list_get_slice() -> None:
    assert arg_list_012[0:2] == arg_list_01
    assert arg_list_012[0:3] == arg_list_012
    assert arg_list_012[1:3] == arg_list_12
