from codegen import constraints
from codegen.typing import elem, lmul, misc, vreg


def test_supported_ratio() -> None:
    assert (
        constraints.supported_ratio(misc.param_size_t("kRatio"))
        == "SupportedRatio<kRatio>"
    )


def test_compatible_elem_ratio() -> None:
    assert (
        constraints.compatible_elem_ratio(
            elem.param("E"),
            misc.param_size_t("kRatio"),
        )
        == "CompatibleElemRatio<E, kRatio>"
    )


def test_compatible_vreg_ratio() -> None:
    assert (
        constraints.compatible_vreg_ratio(
            vreg.param("V"),
            misc.param_size_t("kRatio"),
        )
        == "CompatibleVRegRatio<V, kRatio>"
    )


def test_compatible_elem_lmul() -> None:
    assert (
        constraints.compatible_elem_lmul(
            elem.param("E"),
            lmul.param("kLMul"),
        )
        == "CompatibleElemLMul<E, kLMul>"
    )


def test_has_width() -> None:
    assert constraints.has_width(elem.param("E"), 32) == "(sizeof(E) == 4)"


def test_supported_integral_element() -> None:
    assert (
        constraints.supported_integral_element(elem.param("E"))
        == "SupportedIntegralElement<E>"
    )


def test_supported_signed_element() -> None:
    assert (
        constraints.supported_signed_element(elem.param("E"))
        == "SupportedSignedElement<E>"
    )


def test_supported_unsigned_element() -> None:
    assert (
        constraints.supported_unsigned_element(elem.param("E"))
        == "SupportedUnsignedElement<E>"
    )


def test_supported_floating_point_element() -> None:
    assert (
        constraints.supported_floating_point_element(elem.param("E"), True)
        == "SupportedFloatingPointElement<E, true>"
    )
    assert (
        constraints.supported_floating_point_element(elem.param("E"), False)
        == "SupportedFloatingPointElement<E, false>"
    )


def test_supported_integral_vreg() -> None:
    assert (
        constraints.supported_integral_vreg(vreg.param("V"))
        == "SupportedIntegralVReg<V>"
    )


def test_supported_signed_vreg() -> None:
    assert (
        constraints.supported_signed_vreg(vreg.param("V"))
        == "SupportedSignedVReg<V>"
    )


def test_supported_unsigned_vreg() -> None:
    assert (
        constraints.supported_unsigned_vreg(vreg.param("V"))
        == "SupportedUnsignedVReg<V>"
    )


def test_supported_floating_point_vreg() -> None:
    assert (
        constraints.supported_floating_point_vreg(vreg.param("V"), True)
        == "SupportedFloatingPointVReg<V>"
    )
    assert (
        constraints.supported_floating_point_vreg(vreg.param("V"), False)
        == "SupportedFloatingPointVReg<V, false>"
    )
