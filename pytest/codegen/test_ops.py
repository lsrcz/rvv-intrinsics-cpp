import codegen.ops as ops


def test_vadd_vx() -> None:
    f = ops.binary_op("vadd", "int", "vx")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vadd(V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vadd(vs2, rs1, vl);
}"""
    )


def test_vadd_vx_tum() -> None:
    f = ops.binary_op("vadd", "int", "vx")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vadd(vmask_t<kRatio> vm, V vd, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vadd_tum(vm, vd, vs2, rs1, vl);
}"""
    )


def test_vadd_vv_m() -> None:
    f = ops.binary_op("vadd", "int", "vv")
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
    f = ops.binary_op("vadd", "int", "vv")
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
    f = ops.unary_op("vneg", "int")
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
    f = ops.unary_op("vneg", "int")
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
    f = ops.binary_op("vadc", "int", "vx", op_variant="use_carry")
    assert (
        f("tu").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vadc(V vd, V vs2, elem_t<V> rs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vadc_tu(vd, vs2, rs1, v0, vl);
}"""
    )


def test_vmadc_vx() -> None:
    f = ops.binary_op("vmadc", "int", "vx", op_variant="use_and_produce_carry")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmadc(V vs2, elem_t<V> rs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vmadc(vs2, rs1, v0, vl);
}"""
    )


def test_vsbc_vv_tu() -> None:
    f = ops.binary_op("vsbc", "int", "vv", op_variant="use_carry")
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
    f = ops.binary_op("vmadd", "int", "vv", op_variant="use_and_produce_carry")
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
    f = ops.binary_op("vsll", "int", "vv", op_variant="shifting")
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
    f = ops.binary_op("vsra", "signed", "vx", op_variant="shifting")
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
    f = ops.binary_op("vmseq", "int", "vx", op_variant="comparing")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmseq(V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vmseq(vs2, rs1, vl);
}"""
    )


def test_vmseq_vv_tum() -> None:
    f = ops.binary_op("vmseq", "int", "vv", op_variant="comparing")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmseq(vmask_t<kRatio> vm, vmask_t<kRatio> vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vmseq_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vmsltu_vx_tum() -> None:
    f = ops.binary_op("vmsltu", "unsigned", "vx", op_variant="comparing")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmsltu(V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vmsltu(vs2, rs1, vl);
}"""
    )
