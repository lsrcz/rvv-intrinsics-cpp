from codegen.typing import elem, misc


def test_non_const_ptr_type() -> None:
    ptr = misc.ptr(elem.int32_t, is_const=False)
    assert ptr.cpp_repr == "int32_t *"


def test_const_ptr_type() -> None:
    ptr = misc.ptr(elem.int32_t, is_const=True)
    assert ptr.cpp_repr == "const int32_t *"


def test_void_type() -> None:
    assert misc.void.cpp_repr == "void"


def test_size_t_type() -> None:
    assert misc.size_t.cpp_repr == "size_t"


def test_lit_size_t_value() -> None:
    assert misc.lit_size_t(42).cpp_repr == "42"


def test_param_size_t_value() -> None:
    param = misc.param_size_t("kRatio")
    assert param.kind == misc.size_t_kind
    assert param.cpp_repr == "kRatio"


def test_ptrdiff_t_type() -> None:
    assert misc.ptrdiff_t.cpp_repr == "ptrdiff_t"
