from codegen.type import vl


def test_vl() -> None:
    assert vl.VLType(ratio=32).cpp_repr == "vl_t<32>"
