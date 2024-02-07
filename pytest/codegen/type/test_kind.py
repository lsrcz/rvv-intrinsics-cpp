from codegen.typing import kind


def test_type_kind() -> None:
    assert kind.type_kind.cpp_repr == "typename"
