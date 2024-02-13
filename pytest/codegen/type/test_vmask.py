from codegen.typing import misc, vmask


def test_vmask() -> None:
    assert vmask.concrete(misc.lit_size_t(32)).cpp_repr == "vmask_t<32>"
    assert (
        vmask.concrete(misc.param_size_t("kRatio")).cpp_repr
        == "vmask_t<kRatio>"
    )
