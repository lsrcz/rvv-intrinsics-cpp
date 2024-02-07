from codegen.typing import elem, kind


def test_int_type_signed() -> None:
    int8_t = elem.int8_t
    assert int8_t.long_name == "int8"
    assert int8_t.short_name == "i8"
    assert int8_t.element_width == 8
    assert int8_t.cpp_repr == "int8_t"


def test_int_type_unsigned() -> None:
    int64_t = elem.uint64_t
    assert int64_t.long_name == "uint64"
    assert int64_t.short_name == "u64"
    assert int64_t.element_width == 64
    assert int64_t.cpp_repr == "uint64_t"


def test_float_type() -> None:
    float32_t = elem.float32_t
    assert float32_t.long_name == "float32"
    assert float32_t.short_name == "f32"
    assert float32_t.element_width == 32
    assert float32_t.cpp_repr == "float32_t"


def test_param_elem_type() -> None:
    param_elem = elem.param("E")
    assert param_elem.cpp_repr == "E"
    assert param_elem.kind == kind.type_kind
    assert param_elem.typename == "E"
