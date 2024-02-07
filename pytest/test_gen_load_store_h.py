import gen_load_store_h
from codegen.typing import elem, misc


def test_vle_base_def_int8_ratio8() -> None:
    res = gen_load_store_h.non_indexed_load_base_def_template(
        "vle",
    )(
        "",
        elem.IntType(width=8, signed=True),
        misc.LitSizeTValue(value=8),
    )
    assert res is not None
    assert (
        res.cpp_repr
        == """RVV_ALWAYS_INLINE
vreg_t<int8_t, 8> vle(const int8_t * rs1, vl_t<8> vl) {
  return __riscv_vle8_v_i8m1(rs1, vl);
}"""
    )


def test_vle_base_def_int8_ratio64() -> None:
    res = gen_load_store_h.non_indexed_load_base_def_template(
        "vle",
    )(
        "",
        elem.IntType(width=8, signed=True),
        misc.LitSizeTValue(value=64),
    )
    assert res is not None
    assert (
        res.cpp_repr
        == """#if HAS_ELEN64
RVV_ALWAYS_INLINE
vreg_t<int8_t, 64> vle(const int8_t * rs1, vl_t<64> vl) {
  return __riscv_vle8_v_i8mf8(rs1, vl);
}
#endif"""
    )


def test_vle_base_def_int64_ratio8() -> None:
    res = gen_load_store_h.non_indexed_load_base_def_template(
        "vle",
    )(
        "",
        elem.IntType(width=64, signed=True),
        misc.LitSizeTValue(value=8),
    )
    assert res is not None
    assert (
        res.cpp_repr
        == """#if HAS_ZVE64X
RVV_ALWAYS_INLINE
vreg_t<int64_t, 8> vle(const int64_t * rs1, vl_t<8> vl) {
  return __riscv_vle64_v_i64m8(rs1, vl);
}
#endif"""
    )


def test_vlse_base_def_int8_ratio8() -> None:
    res = gen_load_store_h.non_indexed_load_base_def_template(
        "vlse",
    )(
        "",
        elem.IntType(width=8, signed=True),
        misc.LitSizeTValue(value=8),
    )
    assert res is not None
    assert (
        res.cpp_repr
        == """RVV_ALWAYS_INLINE
vreg_t<int8_t, 8> vlse(const int8_t * rs1, ptrdiff_t rs2, vl_t<8> vl) {
  return __riscv_vlse8_v_i8m1(rs1, rs2, vl);
}"""
    )


def test_vleff_base_def_int8_ratio8() -> None:
    res = gen_load_store_h.non_indexed_load_base_def_template(
        "vleff",
    )(
        "",
        elem.IntType(width=8, signed=True),
        misc.LitSizeTValue(value=8),
    )
    assert res is not None
    assert (
        res.cpp_repr
        == """RVV_ALWAYS_INLINE
vreg_t<int8_t, 8> vleff(const int8_t * rs1, vl_t<8> * vl) {
  return __riscv_vle8ff_v_i8m1(rs1, &vl->vl, vl->vl);
}"""
    )


def test_vle_m_def_8() -> None:
    res = gen_load_store_h.non_indexed_load_variant_def_template(
        "vle",
    )("m", 8)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires (sizeof(E) == 1) && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vle(vmask_t<kRatio> vm, const E * rs1, vl_t<kRatio> vl) {
  return __riscv_vle8(vm, rs1, vl);
}"""
    )


def test_vle_tum_def_64() -> None:
    res = gen_load_store_h.non_indexed_load_variant_def_template(
        "vle",
    )("tum", 64)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires (sizeof(E) == 8) && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vle(vmask_t<kRatio> vm, vreg_t<E, kRatio> vd, const E * rs1, vl_t<kRatio> vl) {
  return __riscv_vle64_tum(vm, vd, rs1, vl);
}"""
    )


def test_vleff_tumu_def_8() -> None:
    res = gen_load_store_h.non_indexed_load_variant_def_template(
        "vleff",
    )("tumu", 8)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires (sizeof(E) == 1) && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vleff(vmask_t<kRatio> vm, vreg_t<E, kRatio> vd, const E * rs1, vl_t<kRatio> * vl) {
  return __riscv_vle8ff_tumu(vm, vd, rs1, &vl->vl, vl->vl);
}"""
    )


def test_vse_base_def_8() -> None:
    res = gen_load_store_h.non_indexed_store_def_template(
        "vse",
    )("", 8)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires (sizeof(E) == 1) && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
void vse(E * rs1, vreg_t<E, kRatio> vs3, vl_t<kRatio> vl) {
  __riscv_vse8(rs1, vs3, vl);
}"""
    )


def test_vsse_m_def_64() -> None:
    res = gen_load_store_h.non_indexed_store_def_template(
        "vsse",
    )("m", 64)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires (sizeof(E) == 8) && is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
void vsse(vmask_t<kRatio> vm, E * rs1, ptrdiff_t rs2, vreg_t<E, kRatio> vs3, vl_t<kRatio> vl) {
  __riscv_vsse64(vm, rs1, rs2, vs3, vl);
}"""
    )


def test_vlm_8() -> None:
    res = gen_load_store_h.vlm_defs("", misc.LitSizeTValue(value=8))
    assert res is not None
    assert (
        res.cpp_repr
        == """RVV_ALWAYS_INLINE
vmask_t<8> vlm(const uint8_t * rs1, vl_t<8> vl) {
  return __riscv_vlm_v_b8(rs1, vl);
}"""
    )


def test_vlm_64() -> None:
    res = gen_load_store_h.vlm_defs("", misc.LitSizeTValue(value=64))
    assert res is not None
    assert (
        res.cpp_repr
        == """#if HAS_ELEN64
RVV_ALWAYS_INLINE
vmask_t<64> vlm(const uint8_t * rs1, vl_t<64> vl) {
  return __riscv_vlm_v_b64(rs1, vl);
}
#endif"""
    )


def test_vloxei_8() -> None:
    res = gen_load_store_h.vlxei_defs("vloxei")("", 8)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vloxei(const E * rs1, vreg_t<uint8_t, kRatio> rs2, vl_t<kRatio> vl) {
  return __riscv_vloxei8(rs1, rs2, vl);
}"""
    )


def test_vluxei_tum_64() -> None:
    res = gen_load_store_h.vlxei_defs("vluxei")("tum", 8)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
vreg_t<E, kRatio> vluxei(vmask_t<kRatio> vm, vreg_t<E, kRatio> vd, const E * rs1, vreg_t<uint8_t, kRatio> rs2, vl_t<kRatio> vl) {
  return __riscv_vluxei8_tum(vm, vd, rs1, rs2, vl);
}"""
    )


def test_vsoxei_8() -> None:
    res = gen_load_store_h.vsxei_defs("vsoxei")("", 8)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
void vsoxei(E * rs1, vreg_t<uint8_t, kRatio> rs2, vreg_t<E, kRatio> vs3, vl_t<kRatio> vl) {
  __riscv_vsoxei8(rs1, rs2, vs3, vl);
}"""
    )


def test_vsuxei_m_64() -> None:
    res = gen_load_store_h.vsxei_defs("vsuxei")("m", 8)
    assert res is not None
    assert (
        res.cpp_repr
        == """template <typename E, size_t kRatio>
  requires is_compatible_elem_ratio<E, kRatio>
RVV_ALWAYS_INLINE
void vsuxei(vmask_t<kRatio> vm, E * rs1, vreg_t<uint8_t, kRatio> rs2, vreg_t<E, kRatio> vs3, vl_t<kRatio> vl) {
  __riscv_vsuxei8(vm, rs1, rs2, vs3, vl);
}"""
    )
