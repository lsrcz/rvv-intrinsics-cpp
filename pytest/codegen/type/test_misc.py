from codegen.type import elem
from codegen.type import misc


def test_non_const_ptr_type() -> None:
    ptr = misc.PtrType(
        base_type=elem.IntType(width=32, signed=True), is_const=False
    )
    assert ptr.cpp_repr == "int32_t *"


def test_const_ptr_type() -> None:
    ptr = misc.PtrType(
        base_type=elem.IntType(width=32, signed=True), is_const=True
    )
    assert ptr.cpp_repr == "const int32_t *"


def test_void_type() -> None:
    assert misc.VoidType().cpp_repr == "void"


def test_size_t_type() -> None:
    assert misc.SizeTType().cpp_repr == "size_t"


def test_lit_size_t_value() -> None:
    assert misc.LitSizeTValue(value=42).cpp_repr == "42"


def test_param_size_t_value() -> None:
    param = misc.ParamSizeTValue(typename="kRatio")
    assert param.kind == misc.size_t_kind
    assert param.cpp_repr == "kRatio"


def test_ptrdiff_t_type() -> None:
    assert misc.PtrdiffTType().cpp_repr == "ptrdiff_t"
