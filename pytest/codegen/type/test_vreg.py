from codegen.typing import elem, misc, vreg


def test_concrete_vreg_type() -> None:
    v: vreg.ConcreteVRegType = vreg.ConcreteVRegType(
        elem_type=elem.ParamElemType(typename="E"),
        ratio=misc.ParamSizeTValue(typename="kRatio"),
    )
    assert v.cpp_repr == "vreg_t<E, kRatio>"


def test_raw_vreg_type() -> None:
    v: vreg.RawVRegType = vreg.RawVRegType(
        elem_type=elem.IntType(width=32, signed=True),
        ratio=misc.LitSizeTValue(value=32),
    )
    assert v.cpp_repr == "vreg_t<int32_t, 32>"


def test_param_vreg_type() -> None:
    param_vreg = vreg.ParamVRegType(typename="V")
    assert param_vreg.cpp_repr == "V"
    assert param_vreg.kind == vreg.k.TypeKind()
    assert param_vreg.typename == "V"


def test_widen_vreg_type() -> None:
    widen_vreg = vreg.WidenVRegType(
        base_type=vreg.ConcreteVRegType(
            elem_type=elem.ParamElemType(typename="E"),
            ratio=misc.ParamSizeTValue(typename="kRatio"),
        )
    )
    assert widen_vreg.cpp_repr == "widen_t<vreg_t<E, kRatio>>"


def test_widen_n_vreg_type() -> None:
    widen_n_vreg = vreg.WidenNVRegType(
        n=4,
        base_type=vreg.ConcreteVRegType(
            elem_type=elem.ParamElemType(typename="E"),
            ratio=misc.ParamSizeTValue(typename="kRatio"),
        ),
    )
    assert widen_n_vreg.cpp_repr == "widen_n_t<4, vreg_t<E, kRatio>>"
