import gen_int_h


def test_vadd_vx() -> None:
    f = gen_int_h.simple_vx_op("vadd", "int")
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
    f = gen_int_h.simple_vx_op("vadd", "int")
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
    f = gen_int_h.simple_vv_op("vadd", "int")
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
    f = gen_int_h.simple_vv_op("vadd", "int")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vadd(vmask_t<kRatio> vm, V vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vadd_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vwadd_wx_m() -> None:
    f = gen_int_h.widening_wx_op("vwadd", signed=True)
    assert (
        f("m").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && narrowable<V> && is_compatible_vreg_ratio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
V vwadd(vmask_t<kRatio> vm, V vs2, elem_t<narrow_t<V>> rs1, vl_t<kRatio> vl) {
  return __riscv_vwadd_wx(vm, vs2, rs1, vl);
}"""
    )


def test_vwaddu_vx_tum() -> None:
    f = gen_int_h.widening_vx_op("vwadd", signed=False)
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable<V> && is_compatible_vreg_ratio<widen_t<V>, kRatio>
RVV_ALWAYS_INLINE
widen_t<V> vwaddu(vmask_t<kRatio> vm, widen_t<V> vd, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vwaddu_vx_tum(vm, vd, vs2, rs1, vl);
}"""
    )


def test_vwadd_wv_m() -> None:
    f = gen_int_h.widening_wv_op("vwadd", signed=True)
    assert (
        f("m").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && narrowable<V> && is_compatible_vreg_ratio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
V vwadd(vmask_t<kRatio> vm, V vs2, narrow_t<V> vs1, vl_t<kRatio> vl) {
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
widen_t<V> vwaddu(vmask_t<kRatio> vm, widen_t<V> vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vwaddu_vv_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vneg_v() -> None:
    f = gen_int_h.simple_v_op("vneg", "int")
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
    f = gen_int_h.simple_v_op("vneg", "int")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vneg(vmask_t<kRatio> vm, V vd, V vs, vl_t<kRatio> vl) {
  return __riscv_vneg_tum(vm, vd, vs, vl);
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
widen_t<V> vwcvtu(vmask_t<kRatio> vm, widen_t<V> vd, V vs2, vl_t<kRatio> vl) {
  return __riscv_vwcvtu_x_tum(vm, vd, vs2, vl);
}"""
    )


def test_vsext2() -> None:
    f = gen_int_h.extending_op("vsext")
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
    f = gen_int_h.extending_op("vzext")
    assert (
        f("tum", 8).cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && widenable_n<8, V> && is_compatible_vreg_ratio<widen_n_t<8, V>, kRatio>
RVV_ALWAYS_INLINE
widen_n_t<8, V> vzext8(vmask_t<kRatio> vm, widen_n_t<8, V> vd, V vs2, vl_t<kRatio> vl) {
  return __riscv_vzext_vf8_tum(vm, vd, vs2, vl);
}"""
    )


def test_vsbc_vv_tu() -> None:
    f = gen_int_h.add_sub_carry_vvm_op("vsbc")
    assert (
        f("tu").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vsbc(V vd, V vs2, V vs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vsbc_tu(vd, vs2, vs1, v0, vl);
}"""
    )


def test_vadc_vxm_tu() -> None:
    f = gen_int_h.add_sub_carry_vxm_op("vadc")
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
    f = gen_int_h.carry_out_vx_op("vmadc")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmadc(V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vmadc(vs2, rs1, vl);
}"""
    )


def test_vmsbc_vv() -> None:
    f = gen_int_h.carry_out_vv_op("vmadd")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmadd(V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vmadd(vs2, vs1, vl);
}"""
    )


def test_vmadc_vxm() -> None:
    f = gen_int_h.carry_out_vxm_op("vmadc")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmadc(V vs2, elem_t<V> rs1, vmask_t<kRatio> v0, vl_t<kRatio> vl) {
  return __riscv_vmadc(vs2, rs1, v0, vl);
}"""
    )


def test_vmsbc_vvm() -> None:
    f = gen_int_h.carry_out_vvm_op("vmadd")
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
    f = gen_int_h.shifting_vv_op("vsll")
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
    f = gen_int_h.shifting_vx_op("vsra")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vsra(vmask_t<kRatio> vm, V vd, V vs2, size_t rs1, vl_t<kRatio> vl) {
  return __riscv_vsra_tum(vm, vd, vs2, rs1, vl);
}"""
    )


def test_vsrl_vv_m() -> None:
    f = gen_int_h.shifting_vv_op("vsrl")
    assert (
        f("m").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vsrl(vmask_t<kRatio> vm, V vs2, to_unsigned_t<V> vs1, vl_t<kRatio> vl) {
  return __riscv_vsrl(vm, vs2, vs1, vl);
}"""
    )


def test_vnsra_wx_tumu() -> None:
    f = gen_int_h.narrowing_shift_wx_op("vnsra")
    assert (
        f("tumu").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio> && narrowable<V> && is_compatible_vreg_ratio<narrow_t<V>, kRatio>
RVV_ALWAYS_INLINE
narrow_t<V> vnsra(vmask_t<kRatio> vm, narrow_t<V> vd, V vs2, size_t rs1, vl_t<kRatio> vl) {
  return __riscv_vnsra_tumu(vm, vd, vs2, rs1, vl);
}"""
    )


def test_vnsrl_wx() -> None:
    f = gen_int_h.narrowing_shift_wx_op("vnsrl")
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
    f = gen_int_h.narrowing_shift_wv_op("vnsra")
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
    f = gen_int_h.narrowing_shift_wv_op("vnsrl")
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


def test_vmseq_vx() -> None:
    f = gen_int_h.comparing_vx_op("vmseq")
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
    f = gen_int_h.comparing_vv_op("vmseq")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_integral_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmseq(vmask_t<kRatio> vm, vmask_t<kRatio> vd, V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vmseq_tum(vm, vd, vs2, vs1, vl);
}"""
    )


def test_vmsltu_vx() -> None:
    f = gen_int_h.comparing_vx_op("vmsltu")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmsltu(V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vmsltu(vs2, rs1, vl);
}"""
    )


def test_vmsgt_vv() -> None:
    f = gen_int_h.comparing_vv_op("vmsgt")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
vmask_t<kRatio> vmsgt(V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vmsgt(vs2, vs1, vl);
}"""
    )


def test_vmin_vv() -> None:
    f = gen_int_h.vv_min_max_op("vmin")
    assert (
        f("").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_signed_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vmin(V vs2, V vs1, vl_t<kRatio> vl) {
  return __riscv_vmin(vs2, vs1, vl);
}"""
    )


def test_vmaxu_vx_tum() -> None:
    f = gen_int_h.vx_min_max_op("vmaxu")
    assert (
        f("tum").cpp_repr
        == """template <typename V, size_t kRatio>
  requires is_supported_unsigned_vreg<V> && is_compatible_vreg_ratio<V, kRatio>
RVV_ALWAYS_INLINE
V vmaxu(vmask_t<kRatio> vm, V vd, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) {
  return __riscv_vmaxu_tum(vm, vd, vs2, rs1, vl);
}"""
    )
