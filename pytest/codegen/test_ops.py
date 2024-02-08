import codegen.ops as ops


def test_vadd_vx() -> None:
    f = ops.binary_op_template_on_elem("vadd", "int")
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
    f = ops.binary_op_template_on_elem("vadd", "int")
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
    f = ops.binary_op_template_on_vreg("vadd", "int")
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
    f = ops.binary_op_template_on_vreg("vadd", "int")
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


def test_vadc_vx_tu() -> None:
    f = ops.binary_op_template_on_elem("vadc", "int", op_variant="use_carry")
    assert (
        f("tu").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_integral<E> && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vadc(vreg_t<E, kRatio> vd, vreg_t<E, kRatio> vs2, E rs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vadc_tu(vd, vs2, rs1, v0, vl);
}"""
    )


def test_vmadc_vx() -> None:
    f = ops.binary_op_template_on_elem(
        "vmadc", "int", op_variant="use_and_produce_carry"
    )
    assert (
        f("").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_integral<E> && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmadc(vreg_t<E, kRatio> vs2, E rs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vmadc(vs2, rs1, v0, vl);
}"""
    )


def test_vsbc_vv_tu() -> None:
    f = ops.binary_op_template_on_vreg("vsbc", "int", op_variant="use_carry")
    assert (
        f("tu").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vsbc(V vd, V vs2, V vs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vsbc_tu(vd, vs2, vs1, v0, vl);
}"""
    )


def test_vmsbc_vv() -> None:
    f = ops.binary_op_template_on_vreg(
        "vmadd", "int", op_variant="use_and_produce_carry"
    )
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmadd(V vs2, V vs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vmadd(vs2, vs1, v0, vl);
}"""
    )


def test_vsll_vv() -> None:
    f = ops.binary_op_template_on_vreg("vsll", "int", op_variant="shifting")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vsll(V vs2, to_unsigned_t<V> vs1, vl_t<kRatio> vl) {
  return __riscv_vsll(vs2, vs1, vl);
}"""
    )


def test_vsra_vx_tum() -> None:
    f = ops.binary_op_template_on_vreg(
        "vsra", "signed", op_variant="shifting_scalar"
    )
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vsra(vmask_t<kRatio> vm, V vd, V vs2, size_t rs1, vl_t<kRatio> vl) {
  return __riscv_vsra_tum(vm, vd, vs2, rs1, vl);
}"""
    )


def test_vmseq_vx() -> None:
    f = ops.binary_op_template_on_elem("vmseq", "int", op_variant="comparing")
    assert (
        f("").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_integral<E> && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmseq(vreg_t<E, kRatio> vs2, E rs1, vl_t<kRatio> vl) {
  return __riscv_vmseq(vs2, rs1, vl);
}"""
    )


def test_vmseq_vv_tum() -> None:
    f = ops.binary_op_template_on_vreg("vmseq", "int", op_variant="comparing")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmseq(vmask_t<kRatio> vm, vmask_t<kRatio> vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vmseq_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vmsltu_vv_tum() -> None:
    f = ops.binary_op_template_on_elem(
        "vmsltu", "unsigned", op_variant="comparing"
    )
    assert (
        f("").cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_supported_rvv_unsigned<E> && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmsltu(vreg_t<E, kRatio> vs2, E rs1, vl_t<kRatio> vl) {
  return __riscv_vmsltu(vs2, rs1, vl);
}"""
    )
