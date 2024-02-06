from codegen import constraints
from codegen.type import misc, elem, lmul, vreg


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


def test_is_compatible_vreg_ratio() -> None:
    assert (
        constraints.is_compatible_vreg_ratio(
            vreg.ParamVRegType(typename="V"),
            misc.ParamSizeTValue(typename="kRatio"),
        )
        == "is_compatible_vreg_ratio<V, kRatio>"
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


def test_is_supported_rvv_integral() -> None:
    assert (
        constraints.is_supported_rvv_integral(elem.ParamElemType(typename="E"))
        == "is_supported_rvv_integral<E>"
    )


def test_is_supported_rvv_signed() -> None:
    assert (
        constraints.is_supported_rvv_signed(elem.ParamElemType(typename="E"))
        == "is_supported_rvv_signed<E>"
    )


def test_is_supported_rvv_unsigned() -> None:
    assert (
        constraints.is_supported_rvv_unsigned(elem.ParamElemType(typename="E"))
        == "is_supported_rvv_unsigned<E>"
    )


def test_is_supported_rvv_floating_point() -> None:
    assert (
        constraints.is_supported_rvv_floating_point(
            elem.ParamElemType(typename="E"), True
        )
        == "is_supported_rvv_floating_point<E, true>"
    )
    assert (
        constraints.is_supported_rvv_floating_point(
            elem.ParamElemType(typename="E"), False
        )
        == "is_supported_rvv_floating_point<E, false>"
    )


def test_is_supported_integral_vreg() -> None:
    assert (
        constraints.is_supported_integral_vreg(vreg.ParamVRegType(typename="V"))
        == "is_supported_integral_vreg<V>"
    )


def test_is_supported_signed_vreg() -> None:
    assert (
        constraints.is_supported_signed_vreg(vreg.ParamVRegType(typename="V"))
        == "is_supported_signed_vreg<V>"
    )


def test_is_supported_unsigned_vreg() -> None:
    assert (
        constraints.is_supported_unsigned_vreg(vreg.ParamVRegType(typename="V"))
        == "is_supported_unsigned_vreg<V>"
    )


def test_is_supported_floating_point_vreg() -> None:
    assert (
        constraints.is_supported_floating_point_vreg(
            vreg.ParamVRegType(typename="V"), True
        )
        == "is_supported_floating_point_vreg<V, true>"
    )
    assert (
        constraints.is_supported_floating_point_vreg(
            vreg.ParamVRegType(typename="V"), False
        )
        == "is_supported_floating_point_vreg<V, false>"
    )
