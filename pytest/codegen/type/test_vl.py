from codegen.type import vl, misc


def test_vl() -> None:
    assert vl.VLType(ratio=misc.LitSizeTValue(value=32)).cpp_repr == "vl_t<32>"
    assert (
        vl.VLType(ratio=misc.ParamSizeTValue(typename="kRatio")).cpp_repr
        == "vl_t<kRatio>"
    )
