from codegen import cpp_repr
from codegen.typing import misc


def test_cpp_repr_str() -> None:
    assert cpp_repr.to_cpp_repr("foo") == "foo"


def test_cpp_repr_field() -> None:
    assert cpp_repr.to_cpp_repr(misc.SizeTType()) == "size_t"
