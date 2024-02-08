import gen_misc_h


def test_vsetvl_decl() -> None:
    assert (
        gen_misc_h.vsetvl_decl("vsetvl", True)("").cpp_repr
        == """template <size_t kRatio>
  requires SupportedRatio<kRatio>
RVV_ALWAYS_INLINE
vl_t<kRatio> vsetvl(size_t avl);"""
    )


def test_vsetvl_decl_vlmax() -> None:
    assert (
        gen_misc_h.vsetvl_decl("vsetvlmax", False)("").cpp_repr
        == """template <size_t kRatio>
  requires SupportedRatio<kRatio>
RVV_ALWAYS_INLINE
vl_t<kRatio> vsetvlmax();"""
    )


def test_vsetvl_defs_vsetvl_ratio8() -> None:
    assert (
        gen_misc_h.vsetvl_defs("vsetvl", True)(
            "", gen_misc_h.misc.LitSizeTValue(value=8)
        ).cpp_repr
        == """template <>
RVV_ALWAYS_INLINE
vl_t<8> vsetvl(size_t avl) {
  return vl_t<8>{__riscv_vsetvl_e8m1(avl)};
}"""
    )


def test_vsetvl_defs_vsetvl_ratio64() -> None:
    assert (
        gen_misc_h.vsetvl_defs("vsetvl", True)(
            "", gen_misc_h.misc.LitSizeTValue(value=64)
        ).cpp_repr
        == """#if HAS_ELEN64
template <>
RVV_ALWAYS_INLINE
vl_t<64> vsetvl(size_t avl) {
  return vl_t<64>{__riscv_vsetvl_e8mf8(avl)};
}
#endif"""
    )


def test_vsetvl_defs_vsetvlmax_ratio8() -> None:
    assert (
        gen_misc_h.vsetvl_defs("vsetvlmax", False)(
            "", gen_misc_h.misc.LitSizeTValue(value=8)
        ).cpp_repr
        == """template <>
RVV_ALWAYS_INLINE
vl_t<8> vsetvlmax() {
  return vl_t<8>{__riscv_vsetvlmax_e8m1()};
}"""
    )
