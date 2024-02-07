from codegen.param_list import template
from codegen.typing import elem, misc, vreg

import pytest

type_param0 = misc.ParamSizeTValue(typename="type_param0")
type_param1 = elem.ParamElemType(typename="type_param1")
type_param2 = vreg.ParamVRegType(typename="type_param2")

param_list_empty = template.TemplateTypeParamList()
param_list_0 = template.TemplateTypeParamList(type_param0)
param_list_1 = template.TemplateTypeParamList(type_param1)
param_list_01 = template.TemplateTypeParamList(type_param0, type_param1)
param_list_012 = template.TemplateTypeParamList(
    type_param0, type_param1, type_param2
)
param_list_12 = template.TemplateTypeParamList(type_param1, type_param2)


def test_typed_param() -> None:
    assert param_list_0.cpp_repr == "<size_t type_param0>"


@pytest.mark.parametrize(
    "template_param_list,expected",
    [
        (
            param_list_empty,
            "<>",
        ),
        (
            param_list_0,
            "<size_t type_param0>",
        ),
        (
            param_list_01,
            "<size_t type_param0, typename type_param1>",
        ),
    ],
)
def test_template_param_list_cpp_repr(
    template_param_list: template.TemplateTypeParamList, expected: str
) -> None:
    assert template_param_list.cpp_repr == expected


def test_template_param_list_forward() -> None:
    assert param_list_01.forward == template.TemplateTypeArgumentList(
        type_param0, type_param1
    )


def test_template_param_list_add() -> None:
    assert (param_list_0 + param_list_1) == param_list_01


def test_template_param_list_len() -> None:
    assert len(param_list_01) == 2


def test_template_param_list_get_single_item() -> None:
    assert param_list_012[0] == type_param0
    assert param_list_012[1] == type_param1
    assert param_list_012[2] == type_param2


def test_template_param_list_get_slice() -> None:
    assert param_list_012[0:2] == param_list_01
    assert param_list_012[0:3] == param_list_012
    assert param_list_012[1:3] == param_list_12


type0 = misc.LitSizeTValue(value=32)
type1 = elem.FloatType(width=32)
type2 = misc.PtrdiffTType()

arg_list_empty = template.TemplateTypeArgumentList()
arg_list_0 = template.TemplateTypeArgumentList(type0)
arg_list_1 = template.TemplateTypeArgumentList(type1)
arg_list_01 = template.TemplateTypeArgumentList(type0, type1)
arg_list_012 = template.TemplateTypeArgumentList(type0, type1, type2)
arg_list_12 = template.TemplateTypeArgumentList(type1, type2)


@pytest.mark.parametrize(
    "template_arg_list,expected",
    [
        (
            arg_list_empty,
            "<>",
        ),
        (
            arg_list_0,
            "<32>",
        ),
        (
            arg_list_01,
            "<32, float32_t>",
        ),
    ],
)
def test_template_typed_arg_list_cpp_repr(
    template_arg_list: template.TemplateTypeArgumentList, expected: str
) -> None:
    assert template_arg_list.cpp_repr == expected


def test_template_typed_arg_list_add() -> None:
    assert (arg_list_0 + arg_list_1) == arg_list_01


def test_template_typed_arg_list_len() -> None:
    assert len(arg_list_01) == 2


def test_template_typed_arg_list_get_single_item() -> None:
    assert arg_list_012[0] == type0
    assert arg_list_012[1] == type1
    assert arg_list_012[2] == type2


def test_template_typed_arg_list_get_slice() -> None:
    assert arg_list_012[0:2] == arg_list_01
    assert arg_list_012[0:3] == arg_list_012
    assert arg_list_012[1:3] == arg_list_12
