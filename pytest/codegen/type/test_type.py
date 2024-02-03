from codegen.type import type
from codegen.type import misc


def test_data_kind() -> None:
    assert type.DataKind(data_type=misc.SizeTType()).cpp_repr == "size_t"
