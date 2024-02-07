from codegen import validate
from codegen.typing import elem, lmul, misc

import pytest

elem_ratio_lmul_test: pytest.MarkDecorator = pytest.mark.parametrize(
    "elem_type,ratio,lmul_value",
    [
        (elem.int8_t, 64, -3),
        (elem.int16_t, 64, -2),
        (elem.int64_t, 64, 0),
        (elem.int64_t, 8, 3),
        (elem.int8_t, 1, 3),
        (elem.int16_t, 2, 3),
        (elem.float16_t, 2, 3),
        (elem.float32_t, 4, 3),
    ],
)


@elem_ratio_lmul_test
def test_elem_ratio_to_lmul(
    elem_type: elem.RawElemType, ratio: int, lmul_value: int
) -> None:
    assert validate.elem_ratio_to_lmul(
        elem_type, misc.lit_size_t(ratio)
    ) == lmul.lit(lmul_value)


@elem_ratio_lmul_test
def test_elem_lmul_to_ratio(
    elem_type: elem.RawElemType, ratio: int, lmul_value: int
) -> None:
    assert validate.elem_ratio_to_lmul(
        elem_type, misc.lit_size_t(ratio)
    ) == lmul.lit(lmul_value)


@pytest.mark.parametrize(
    "elem_type,ratio,expected",
    [
        (elem.int8_t, 64, True),
        (elem.int16_t, 64, True),
        (elem.int64_t, 64, True),
        (elem.int8_t, 8, True),
        (elem.int16_t, 8, True),
        (elem.int64_t, 8, True),
        (elem.int8_t, 4, True),
        (elem.int32_t, 4, True),
        (elem.int64_t, 4, False),
        (elem.int8_t, 1, True),
        (elem.int16_t, 1, False),
        (elem.int64_t, 1, False),
        (elem.float16_t, 8, True),
        (elem.float32_t, 8, True),
        (elem.float64_t, 8, True),
    ],
)
def test_is_compatible_elem_ratio(
    elem_type: elem.RawElemType, ratio: int, expected: lmul.LMul
) -> None:
    assert (
        validate.is_compatible_elem_ratio_may_under_guards(
            elem_type, misc.lit_size_t(ratio)
        )
        == expected
    )


@pytest.mark.parametrize(
    "elem_type,lmul_value,expected",
    [
        (elem.int8_t, 3, True),
        (elem.int8_t, 0, True),
        (elem.int8_t, -3, True),
        (elem.int16_t, 3, True),
        (elem.int16_t, 0, True),
        (elem.int16_t, -2, True),
        (elem.int16_t, -3, False),
        (elem.int64_t, 3, True),
        (elem.int64_t, 0, True),
        (elem.int64_t, -1, False),
        (elem.int64_t, -3, False),
    ],
)
def test_is_compatible_elem_lmul(
    elem_type: elem.RawElemType, lmul_value: int, expected: bool
) -> None:
    assert (
        validate.is_compatible_elem_lmul_may_under_guards(
            elem_type, lmul.lit(lmul_value)
        )
        == expected
    )
