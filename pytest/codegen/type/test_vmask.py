from codegen.type import vmask


def test_vmask() -> None:
    assert vmask.VMaskType(ratio=32).cpp_repr == "vmask_t<32>"
