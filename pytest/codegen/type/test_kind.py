from codegen.type import kind


def test_type_kind() -> None:
    assert kind.TypeKind().cpp_repr == "typename"
