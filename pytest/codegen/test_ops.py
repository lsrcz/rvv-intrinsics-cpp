import codegen.ops as ops


def test_vadd_vx() -> None:
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


def test_vadd_vx_tum() -> None:
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


def test_vadc_vx() -> None:
    f = ops.vx_op("vadc", "int", with_carry=True)
    assert (
        f("").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_integral<E> && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vadc(vreg_t<E, kRatio> vs2, E rs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vadc(vs2, rs1, v0, vl);
}"""
    )


def test_vmadc_vx_tum() -> None:
    f = ops.vx_op("vmadd", "int", with_carry=True, return_carry=True)
    assert (
        f("tu").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_integral<E> && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmadd(vreg_t<E, kRatio> vd, vreg_t<E, kRatio> vs2, E rs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vmadd_tu(vd, vs2, rs1, v0, vl);
}"""
    )


def test_vsbc_vv() -> None:
    f = ops.vv_op("vsbc", "int", with_carry=True)
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vsbc(V vs2, V vs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vsbc(vs2, vs1, v0, vl);
}"""
    )


def test_vmsbc_vv_tum() -> None:
    f = ops.vv_op("vmadd", "int", with_carry=True, return_carry=True)
    assert (
        f("tu").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmadd(V vd, V vs2, V vs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vmadd_tu(vd, vs2, vs1, v0, vl);
}"""
    )
