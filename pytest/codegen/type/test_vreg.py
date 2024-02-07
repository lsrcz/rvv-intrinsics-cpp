from codegen.typing import elem, misc, vreg, kind


def test_concrete_vreg_type() -> None:
    v = vreg.concrete(
        elem.param("E"),
        misc.param_size_t("kRatio"),
    )
    assert v.cpp_repr == "vreg_t<E, kRatio>"


def test_raw_vreg_type() -> None:
    v: vreg.RawVRegType = vreg.raw(
        elem.int32_t,
        misc.lit_size_t(32),
    )
    assert v.cpp_repr == "vreg_t<int32_t, 32>"


def test_param_vreg_type() -> None:
    param_vreg = vreg.param("V")
    assert param_vreg.cpp_repr == "V"
    assert param_vreg.kind == kind.type_kind
    assert param_vreg.typename == "V"


def test_widen_vreg_type() -> None:
    widen_vreg = vreg.widen(
        vreg.concrete(
            elem.param("E"),
            misc.param_size_t("kRatio"),
        )
    )
    assert widen_vreg.cpp_repr == "widen_t<vreg_t<E, kRatio>>"


def test_widen_n_vreg_type() -> None:
    widen_n_vreg = vreg.widen_n(
        4,
        vreg.concrete(
            elem.param("E"),
            misc.param_size_t("kRatio"),
        ),
    )
    assert widen_n_vreg.cpp_repr == "widen_n_t<4, vreg_t<E, kRatio>>"
