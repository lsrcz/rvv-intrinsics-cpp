from codegen import validate
from codegen.typing import elem, lmul, misc

import pytest

elem_ratio_lmul_test: pytest.MarkDecorator = pytest.mark.parametrize(
    "elem_type,ratio,lmul_value",
    [
        (elem.IntType(width=8, signed=True), 64, lmul.LMul(lmul=-3)),
        (elem.IntType(width=16, signed=True), 64, lmul.LMul(lmul=-2)),
        (elem.IntType(width=64, signed=True), 64, lmul.LMul(lmul=0)),
        (elem.IntType(width=64, signed=True), 8, lmul.LMul(lmul=3)),
        (elem.IntType(width=8, signed=True), 1, lmul.LMul(lmul=3)),
        (elem.IntType(width=16, signed=True), 2, lmul.LMul(lmul=3)),
        (elem.FloatType(width=16), 2, lmul.LMul(lmul=3)),
        (elem.FloatType(width=32), 4, lmul.LMul(lmul=3)),
    ],
)


@elem_ratio_lmul_test
def test_elem_ratio_to_lmul(
    elem_type: elem.RawElemType, ratio: int, lmul_value: lmul.LMul
) -> None:
    assert validate.elem_ratio_to_lmul(
        elem_type, misc.LitSizeTValue(value=ratio)
    ) == lmul.LitLMulValue(lmul=lmul_value)


@elem_ratio_lmul_test
def test_elem_lmul_to_ratio(
    elem_type: elem.RawElemType, ratio: int, lmul_value: lmul.LMul
) -> None:
    assert validate.elem_ratio_to_lmul(
        elem_type, misc.LitSizeTValue(value=ratio)
    ) == lmul.LitLMulValue(lmul=lmul_value)


@pytest.mark.parametrize(
    "elem_type,ratio,expected",
    [
        (elem.IntType(width=8, signed=True), 64, True),
        (elem.IntType(width=16, signed=True), 64, True),
        (elem.IntType(width=64, signed=True), 64, True),
        (elem.IntType(width=8, signed=True), 8, True),
        (elem.IntType(width=16, signed=True), 8, True),
        (elem.IntType(width=64, signed=True), 8, True),
        (elem.IntType(width=8, signed=True), 4, True),
        (elem.IntType(width=32, signed=True), 4, True),
        (elem.IntType(width=64, signed=True), 4, False),
        (elem.IntType(width=8, signed=True), 1, True),
        (elem.IntType(width=16, signed=True), 1, False),
        (elem.IntType(width=64, signed=True), 1, False),
        (elem.FloatType(width=16), 8, True),
        (elem.FloatType(width=32), 8, True),
        (elem.FloatType(width=64), 8, True),
    ],
)
def test_is_compatible_elem_ratio(
    elem_type: elem.RawElemType, ratio: int, expected: lmul.LMul
) -> None:
    assert (
        validate.is_compatible_elem_ratio_may_under_guards(
            elem_type, misc.LitSizeTValue(value=ratio)
        )
        == expected
    )


@pytest.mark.parametrize(
    "elem_type,lmul_value,expected",
    [
        (elem.IntType(width=8, signed=True), lmul.LMul(lmul=3), True),
        (elem.IntType(width=8, signed=True), lmul.LMul(lmul=0), True),
        (elem.IntType(width=8, signed=True), lmul.LMul(lmul=-3), True),
        (elem.IntType(width=16, signed=True), lmul.LMul(lmul=3), True),
        (elem.IntType(width=16, signed=True), lmul.LMul(lmul=0), True),
        (elem.IntType(width=16, signed=True), lmul.LMul(lmul=-2), True),
        (elem.IntType(width=16, signed=True), lmul.LMul(lmul=-3), False),
        (elem.IntType(width=64, signed=True), lmul.LMul(lmul=3), True),
        (elem.IntType(width=64, signed=True), lmul.LMul(lmul=0), True),
        (elem.IntType(width=64, signed=True), lmul.LMul(lmul=-1), False),
        (elem.IntType(width=64, signed=True), lmul.LMul(lmul=-3), False),
    ],
)
def test_is_compatible_elem_lmul(
    elem_type: elem.RawElemType, lmul_value: lmul.LMul, expected: bool
) -> None:
    assert (
        validate.is_compatible_elem_lmul_may_under_guards(
            elem_type, lmul.LitLMulValue(lmul=lmul_value)
        )
        == expected
    )
