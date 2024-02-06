from codegen import constraints
from codegen.type import misc, elem, lmul


def test_is_supported_ratio() -> None:
    assert (
        constraints.is_supported_ratio(misc.ParamSizeTValue(typename="kRatio"))
        == "is_supported_ratio<kRatio>"
    )


def test_is_compatible_elem_ratio() -> None:
    assert (
        constraints.is_compatible_elem_ratio(
            elem.ParamElemType(typename="E"),
            misc.ParamSizeTValue(typename="kRatio"),
        )
        == "is_compatible_elem_ratio<E, kRatio>"
    )


def test_is_compatible_elem_lmul() -> None:
    assert (
        constraints.is_compatible_elem_lmul(
            elem.ParamElemType(typename="E"),
            lmul.ParamLMulValueType(typename="kLMul"),
        )
        == "is_compatible_elem_lmul<E, kLMul>"
    )


def test_has_width() -> None:
    assert (
        constraints.has_width(elem.ParamElemType(typename="E"), 32)
        == "(sizeof(E) == 4)"
    )
