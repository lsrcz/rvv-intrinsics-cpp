from codegen.typing import base, misc


def test_data_kind() -> None:
    assert base.DataKind(data_type=misc.SizeTType()).cpp_repr == "size_t"
