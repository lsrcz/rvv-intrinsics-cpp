import gen_fp_h


def test_vfwadd_wf_m() -> None:
    f = gen_fp_h.widening_wf_op("vfwadd")("m")
    assert (
        f.cpp_repr
        == """template <typename V, size_t kRatio>
  requires SupportedFloatingPointVReg<V, true> && CompatibleVRegRatio<V, kRatio> && Narrowable<V> && CompatibleVRegRatio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
V vfwadd(vmask_t<kRatio> vm, V vs2, elem_t<narrow_t<V>> rs1, vl_t<kRatio> vl) {
  return __riscv_vfwadd_wf(vm, vs2, rs1, vl);
}"""
    )


def test_vfwadd_wv_tum() -> None:
    f = gen_fp_h.widening_wv_op("vfwadd")("tum")
    assert (
        f.cpp_repr
        == """template <typename V, size_t kRatio>
  requires SupportedFloatingPointVReg<V, true> && CompatibleVRegRatio<V, kRatio> && Narrowable<V> && CompatibleVRegRatio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
V vfwadd(vmask_t<kRatio> vm, V vd, V vs2, narrow_t<V> vs1, vl_t<kRatio> vl) {
  return __riscv_vfwadd_wv_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vfwsub_vf_tu() -> None:
    f = gen_fp_h.widening_vf_op("vfwsub")("tu")
    assert (
        f.cpp_repr
        == """template <typename V, size_t kRatio>
  requires SupportedFloatingPointVReg<V, true> && CompatibleVRegRatio<V, kRatio> && Widenable<V> && CompatibleVRegRatio<widen_t<V>, kRatio>
RVV_ALWAYS_INLINE
widen_t<V> vfwsub(widen_t<V> vd, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vfwsub_vf_tu(vd, vs2, rs1, vl);
}"""
    )


def test_vfwadd_vv_tumu() -> None:
    f = gen_fp_h.widening_vv_op("vfwadd")("tumu")
    assert (
        f.cpp_repr
        == """template <typename V, size_t kRatio>
  requires SupportedFloatingPointVReg<V, true> && CompatibleVRegRatio<V, kRatio> && Widenable<V> && CompatibleVRegRatio<widen_t<V>, kRatio>
RVV_ALWAYS_INLINE
widen_t<V> vfwadd(vmask_t<kRatio> vm, widen_t<V> vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vfwadd_vv_tumu(vm, vd, vs2, vs1, vl);
}"""
    )
