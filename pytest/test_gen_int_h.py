import gen_int_h


def test_vwadd_wx_m() -> None:
    f = gen_int_h.widening_wx_op("vwadd", signed=True)
    assert (
        f("m").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_signed<E> && is_compatible_elem_ratio<E, kRatio> && widenable<E> && is_compatible_elem_ratio<widen_t<E>, kRatio>
RVV_ALWAYS_INLINE
vreg_t<widen_t<E>, kRatio> vwadd(vmask_t<kRatio> vm, vreg_t<widen_t<E>, kRatio> vs2, E rs1, vl_t<kRatio> vl) {
  return __riscv_vwadd_wx(vm, vs2, rs1, vl);
}"""
    )


def test_vwaddu_vx_tum() -> None:
    f = gen_int_h.widening_vx_op("vwadd", signed=False)
    assert (
        f("tum").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_unsigned<E> && is_compatible_elem_ratio<E, kRatio> && widenable<E> && is_compatible_elem_ratio<widen_t<E>, kRatio>
RVV_ALWAYS_INLINE
vreg_t<widen_t<E>, kRatio> vwadd(vmask_t<kRatio> vm, vreg_t<widen_t<E>, kRatio> vd, vreg_t<E, kRatio> vs2, E rs1, vl_t<kRatio> vl) {
  return __riscv_vwaddu_vx_tum(vm, vd, vs2, rs1, vl);
}"""
    )


def test_vwadd_wv_m() -> None:
    f = gen_int_h.widening_wv_op("vwadd", signed=True)
    assert (
        f("m").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable<V> && is_compatible_vreg_ratio<widen_t<V>, kRatio>
RVV_ALWAYS_INLINE
widen_t<V> vwadd(vmask_t<kRatio> vm, widen_t<V> vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vwadd_wv(vm, vs2, vs1, vl);
}"""
    )


def test_vwadd_vv_tum() -> None:
    f = gen_int_h.widening_vv_op("vwadd", signed=False)
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable<V> && is_compatible_vreg_ratio<widen_t<V>, kRatio>
RVV_ALWAYS_INLINE
widen_t<V> vwadd(vmask_t<kRatio> vm, widen_t<V> vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vwaddu_vv_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vwcvt_x() -> None:
    f = gen_int_h.widening_op("vwcvt", True)
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable<V> && is_compatible_vreg_ratio<widen_t<V>, kRatio>
RVV_ALWAYS_INLINE
widen_t<V> vwcvt(V vs2, vl_t<kRatio> vl) {
  return __riscv_vwcvt_x(vs2, vl);
}"""
    )


def test_vwcvtu_x_tum() -> None:
    f = gen_int_h.widening_op("vwcvt", False)
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable<V> && is_compatible_vreg_ratio<widen_t<V>, kRatio>
RVV_ALWAYS_INLINE
widen_t<V> vwcvt(vmask_t<kRatio> vm, widen_t<V> vd, V vs2, vl_t<kRatio> vl) {
  return __riscv_vwcvtu_x_tum(vm, vd, vs2, vl);
}"""
    )


def test_vsext2() -> None:
    f = gen_int_h.extending_op("vsext", True)
    assert (
        f("", 2).cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable_n<2, V> && is_compatible_vreg_ratio<widen_n_t<2, V>, kRatio>
RVV_ALWAYS_INLINE
widen_n_t<2, V> vsext2(V vs2, vl_t<kRatio> vl) {
  return __riscv_vsext_vf2(vs2, vl);
}"""
    )


def test_vzext8_tum() -> None:
    f = gen_int_h.extending_op("vzext", False)
    assert (
        f("tum", 8).cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable_n<8, V> && is_compatible_vreg_ratio<widen_n_t<8, V>, kRatio>
RVV_ALWAYS_INLINE
widen_n_t<8, V> vzext8(vmask_t<kRatio> vm, widen_n_t<8, V> vd, V vs2, vl_t<kRatio> vl) {
  return __riscv_vzext_vf8_tum(vm, vd, vs2, vl);
}"""
    )


def test_vnsrl_wx() -> None:
    f = gen_int_h.narrowing_shift_op("vnsrl", op_variant="scalar")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && narrowable<V> && is_compatible_vreg_ratio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
narrow_t<V> vnsrl(V vs2, size_t rs1, vl_t<kRatio> vl) {
  return __riscv_vnsrl(vs2, rs1, vl);
}"""
    )


def test_vnsra_wv_tum() -> None:
    f = gen_int_h.narrowing_shift_op("vnsra")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && narrowable<V> && is_compatible_vreg_ratio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
narrow_t<V> vnsra(vmask_t<kRatio> vm, narrow_t<V> vd, V vs2, narrow_t<to_unsigned_t<V>> vs1, vl_t<kRatio> vl) {
  return __riscv_vnsra_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vnsrl_wv_m() -> None:
    f = gen_int_h.narrowing_shift_op("vnsrl")
    assert (
        f("m").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && narrowable<V> && is_compatible_vreg_ratio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
narrow_t<V> vnsrl(vmask_t<kRatio> vm, V vs2, narrow_t<V> vs1, vl_t<kRatio> vl) {
  return __riscv_vnsrl(vm, vs2, vs1, vl);
}"""
    )


def test_vncvt() -> None:
    assert (
        gen_int_h.vncvt("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && narrowable<V> && is_compatible_vreg_ratio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
narrow_t<V> vncvt(V vs2, vl_t<kRatio> vl) {
  return __riscv_vncvt_x(vs2, vl);
}"""
    )


def test_vncvt_tum() -> None:
    assert (
        gen_int_h.vncvt("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && narrowable<V> && is_compatible_vreg_ratio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
narrow_t<V> vncvt(vmask_t<kRatio> vm, narrow_t<V> vd, V vs2, vl_t<kRatio> vl) {
  return __riscv_vncvt_x_tum(vm, vd, vs2, vl);
}"""
    )
