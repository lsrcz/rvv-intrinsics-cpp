import gen_mask_h
from codegen.typing import elem


def test_viota_decl():
    assert (
        gen_mask_h.mask_vec_ret_op_decl("viota")("").cpp_repr
        == """namespace internal {
template <typename E>
  requires SupportedUnsignedElement<E>
struct viota;
}  // namespace internal
template <typename E>
constexpr inline internal::viota<E> viota{};"""
    )


def test_viota_def():
    assert (
        gen_mask_h.mask_vec_ret_op("viota", elem.unsigned_type(32))("").cpp_repr
        == """namespace internal {
template <>
struct viota<uint32_t> {
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 4> operator()(vmask_t<4> vs2, vl_t<4> vl) const {
  return __riscv_viota_m_u32m8(vs2, vl);
}
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 8> operator()(vmask_t<8> vs2, vl_t<8> vl) const {
  return __riscv_viota_m_u32m4(vs2, vl);
}
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 16> operator()(vmask_t<16> vs2, vl_t<16> vl) const {
  return __riscv_viota_m_u32m2(vs2, vl);
}
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 32> operator()(vmask_t<32> vs2, vl_t<32> vl) const {
  return __riscv_viota_m_u32m1(vs2, vl);
}
#if HAS_ELEN64
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 64> operator()(vmask_t<64> vs2, vl_t<64> vl) const {
  return __riscv_viota_m_u32mf2(vs2, vl);
}
#endif
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 4> operator()(vmask_t<4> vm, vmask_t<4> vs2, vl_t<4> vl) const {
  return __riscv_viota_m_u32m8_m(vm, vs2, vl);
}
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 8> operator()(vmask_t<8> vm, vmask_t<8> vs2, vl_t<8> vl) const {
  return __riscv_viota_m_u32m4_m(vm, vs2, vl);
}
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 16> operator()(vmask_t<16> vm, vmask_t<16> vs2, vl_t<16> vl) const {
  return __riscv_viota_m_u32m2_m(vm, vs2, vl);
}
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 32> operator()(vmask_t<32> vm, vmask_t<32> vs2, vl_t<32> vl) const {
  return __riscv_viota_m_u32m1_m(vm, vs2, vl);
}
#if HAS_ELEN64
RVV_ALWAYS_INLINE
vreg_t<uint32_t, 64> operator()(vmask_t<64> vm, vmask_t<64> vs2, vl_t<64> vl) const {
  return __riscv_viota_m_u32mf2_m(vm, vs2, vl);
}
#endif
};
}  // namespace internal"""
    )
