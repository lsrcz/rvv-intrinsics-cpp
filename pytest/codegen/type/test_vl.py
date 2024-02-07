from codegen.typing import misc, vl


def test_vl() -> None:
    assert vl.vl(misc.lit_size_t(32)).cpp_repr == "vl_t<32>"
    assert (
        vl.vl(misc.param_size_t("kRatio")).cpp_repr
        == "vl_t<kRatio>"
    )
