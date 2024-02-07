from codegen.typing import misc, vmask


def test_vmask() -> None:
    assert vmask.vmask(misc.lit_size_t(32)).cpp_repr == "vmask_t<32>"
    assert (
        vmask.vmask(misc.param_size_t("kRatio")).cpp_repr
        == "vmask_t<kRatio>"
    )
