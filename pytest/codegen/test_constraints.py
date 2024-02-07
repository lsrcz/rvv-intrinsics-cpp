from codegen import constraints
from codegen.typing import elem, lmul, misc, vreg


def test_is_supported_ratio() -> None:
    assert (
        constraints.is_supported_ratio(misc.param_size_t("kRatio"))
        == "is_supported_ratio<kRatio>"
    )


def test_is_compatible_elem_ratio() -> None:
    assert (
        constraints.is_compatible_elem_ratio(
            elem.param("E"),
            misc.param_size_t("kRatio"),
        )
        == "is_compatible_elem_ratio<E, kRatio>"
    )


def test_is_compatible_vreg_ratio() -> None:
    assert (
        constraints.is_compatible_vreg_ratio(
            vreg.param("V"),
            misc.param_size_t("kRatio"),
        )
        == "is_compatible_vreg_ratio<V, kRatio>"
    )


def test_is_compatible_elem_lmul() -> None:
    assert (
        constraints.is_compatible_elem_lmul(
            elem.param("E"),
            lmul.param("kLMul"),
        )
        == "is_compatible_elem_lmul<E, kLMul>"
    )


def test_has_width() -> None:
    assert constraints.has_width(elem.param("E"), 32) == "(sizeof(E) == 4)"


def test_is_supported_rvv_integral() -> None:
    assert (
        constraints.is_supported_rvv_integral(elem.param("E"))
        == "is_supported_rvv_integral<E>"
    )


def test_is_supported_rvv_signed() -> None:
    assert (
        constraints.is_supported_rvv_signed(elem.param("E"))
        == "is_supported_rvv_signed<E>"
    )


def test_is_supported_rvv_unsigned() -> None:
    assert (
        constraints.is_supported_rvv_unsigned(elem.param("E"))
        == "is_supported_rvv_unsigned<E>"
    )


def test_is_supported_rvv_floating_point() -> None:
    assert (
        constraints.is_supported_rvv_floating_point(elem.param("E"), True)
        == "is_supported_rvv_floating_point<E, true>"
    )
    assert (
        constraints.is_supported_rvv_floating_point(elem.param("E"), False)
        == "is_supported_rvv_floating_point<E, false>"
    )


def test_is_supported_integral_vreg() -> None:
    assert (
        constraints.is_supported_integral_vreg(vreg.param("V"))
        == "is_supported_integral_vreg<V>"
    )


def test_is_supported_signed_vreg() -> None:
    assert (
        constraints.is_supported_signed_vreg(vreg.param("V"))
        == "is_supported_signed_vreg<V>"
    )


def test_is_supported_unsigned_vreg() -> None:
    assert (
        constraints.is_supported_unsigned_vreg(vreg.param("V"))
        == "is_supported_unsigned_vreg<V>"
    )


def test_is_supported_floating_point_vreg() -> None:
    assert (
        constraints.is_supported_floating_point_vreg(vreg.param("V"), True)
        == "is_supported_floating_point_vreg<V, true>"
    )
    assert (
        constraints.is_supported_floating_point_vreg(vreg.param("V"), False)
        == "is_supported_floating_point_vreg<V, false>"
    )


def test_widenable_type() -> None:
    assert constraints.widenable_type(elem.param("E")) == "widenable<E>"


def test_widenable_n_type() -> None:
    assert (
        constraints.widenable_n_type(4, elem.param("E")) == "widenable_n<4, E>"
    )
