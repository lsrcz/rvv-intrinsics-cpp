from codegen.type import vreg
from codegen.type import elem
from codegen.type import misc


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
