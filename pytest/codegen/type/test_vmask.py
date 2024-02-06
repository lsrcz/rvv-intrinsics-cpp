from codegen.type import vmask, misc


def test_vmask() -> None:
    assert (
        vmask.VMaskType(ratio=misc.LitSizeTValue(value=32)).cpp_repr
        == "vmask_t<32>"
    )
    assert (
        vmask.VMaskType(ratio=misc.ParamSizeTValue(typename="kRatio")).cpp_repr
        == "vmask_t<kRatio>"
    )
