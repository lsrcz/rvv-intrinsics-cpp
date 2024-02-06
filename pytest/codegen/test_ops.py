import codegen.ops as ops


def test_vadd_vi() -> None:
    f = ops.vx_op("vadd", "int")
    assert (
        f("").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_integral<E> && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vadd(vreg_t<E, kRatio> vs2, E rs1, vl_t<kRatio> vl) {
  return __riscv_vadd(vs2, rs1, vl);
}"""
    )


def test_vadd_vi_tum() -> None:
    f = ops.vx_op("vadd", "int")
    assert (
        f("tum").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_integral<E> && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vadd(vmask_t<kRatio> vm, vreg_t<E, kRatio> vd, vreg_t<E, kRatio> vs2, E rs1, vl_t<kRatio> vl) {
  return __riscv_vadd_tum(vm, vd, vs2, rs1, vl);
}"""
    )


def test_vadd_vv_m() -> None:
    f = ops.vv_op("vadd", "int")
    assert (
        f("m").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vadd(vmask_t<kRatio> vm, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vadd(vm, vs2, vs1, vl);
}"""
    )


def test_vadd_vv_tum() -> None:
    f = ops.vv_op("vadd", "int")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vadd(vmask_t<kRatio> vm, V vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vadd_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vneg_v() -> None:
    f = ops.v_op("vneg", "int")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vneg(V vs, vl_t<kRatio> vl) {
  return __riscv_vneg(vs, vl);
}"""
    )


def test_vneg_v_tum() -> None:
    f = ops.v_op("vneg", "int")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vneg(vmask_t<kRatio> vm, V vd, V vs, vl_t<kRatio> vl) {
  return __riscv_vneg_tum(vm, vd, vs, vl);
}"""
    )


def test_vwadd_wx_m() -> None:
    f = ops.widening_wx_op("vwadd", signed=True)
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
    f = ops.widening_vx_op("vwadd", signed=False)
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
    f = ops.widening_wv_op("vwadd", signed=True)
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
    f = ops.widening_vv_op("vwadd", signed=False)
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable<V> && is_compatible_vreg_ratio<widen_t<V>, kRatio>
RVV_ALWAYS_INLINE
widen_t<V> vwadd(vmask_t<kRatio> vm, widen_t<V> vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vwaddu_vv_tum(vm, vd, vs2, vs1, vl);
}"""
    )
