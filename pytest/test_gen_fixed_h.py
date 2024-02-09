import gen_fixed_h


def test_vaadd():
    c = gen_fixed_h.fixed_arith_op("vaadd")("")
    assert (
        c.cpp_repr
        == """namespace internal {
template <VXRM kVXRM>
  requires SupportedVXRM<kVXRM>
struct vaadd {
template <typename V, size_t kRatio>
  requires SupportedSignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(V vs2, V vs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaadd(vs2, vs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaadd(vs2, vs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaadd(vs2, vs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaadd(vs2, vs1, __RISCV_VXRM_ROD, vl);
  }
}
template <typename V, size_t kRatio>
  requires SupportedSignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(V vs2, elem_t<V> rs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaadd(vs2, rs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaadd(vs2, rs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaadd(vs2, rs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaadd(vs2, rs1, __RISCV_VXRM_ROD, vl);
  }
}
template <typename V, size_t kRatio>
  requires SupportedSignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(vmask_t<kRatio> vm, V vs2, V vs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaadd(vm, vs2, vs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaadd(vm, vs2, vs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaadd(vm, vs2, vs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaadd(vm, vs2, vs1, __RISCV_VXRM_ROD, vl);
  }
}
template <typename V, size_t kRatio>
  requires SupportedSignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(vmask_t<kRatio> vm, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaadd(vm, vs2, rs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaadd(vm, vs2, rs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaadd(vm, vs2, rs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaadd(vm, vs2, rs1, __RISCV_VXRM_ROD, vl);
  }
}
};
}  // namespace internal
template <VXRM kVXRM>
constexpr inline internal::vaadd<kVXRM> vaadd{};"""
    )


def test_vaadd_tumu():
    c = gen_fixed_h.fixed_arith_op("vaadd")("tumu")
    assert (
        c.cpp_repr
        == """namespace internal {
template <VXRM kVXRM>
  requires SupportedVXRM<kVXRM>
struct vaadd {
template <typename V, size_t kRatio>
  requires SupportedSignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(vmask_t<kRatio> vm, V vd, V vs2, V vs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaadd_tumu(vm, vd, vs2, vs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaadd_tumu(vm, vd, vs2, vs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaadd_tumu(vm, vd, vs2, vs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaadd_tumu(vm, vd, vs2, vs1, __RISCV_VXRM_ROD, vl);
  }
}
template <typename V, size_t kRatio>
  requires SupportedSignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(vmask_t<kRatio> vm, V vd, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaadd_tumu(vm, vd, vs2, rs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaadd_tumu(vm, vd, vs2, rs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaadd_tumu(vm, vd, vs2, rs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaadd_tumu(vm, vd, vs2, rs1, __RISCV_VXRM_ROD, vl);
  }
}
};
}  // namespace internal
template <VXRM kVXRM>
constexpr inline internal::vaadd<kVXRM> vaadd{};"""
    )


def test_vaaddu_tu():
    c = gen_fixed_h.fixed_arith_op("vaaddu")("tu")
    assert (
        c.cpp_repr
        == """namespace internal {
template <VXRM kVXRM>
  requires SupportedVXRM<kVXRM>
struct vaaddu {
template <typename V, size_t kRatio>
  requires SupportedUnsignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(V vd, V vs2, V vs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaaddu_tu(vd, vs2, vs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaaddu_tu(vd, vs2, vs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaaddu_tu(vd, vs2, vs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaaddu_tu(vd, vs2, vs1, __RISCV_VXRM_ROD, vl);
  }
}
template <typename V, size_t kRatio>
  requires SupportedUnsignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(V vd, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaaddu_tu(vd, vs2, rs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaaddu_tu(vd, vs2, rs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaaddu_tu(vd, vs2, rs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaaddu_tu(vd, vs2, rs1, __RISCV_VXRM_ROD, vl);
  }
}
template <typename V, size_t kRatio>
  requires SupportedUnsignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(vmask_t<kRatio> vm, V vd, V vs2, V vs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaaddu_tum(vm, vd, vs2, vs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaaddu_tum(vm, vd, vs2, vs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaaddu_tum(vm, vd, vs2, vs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaaddu_tum(vm, vd, vs2, vs1, __RISCV_VXRM_ROD, vl);
  }
}
template <typename V, size_t kRatio>
  requires SupportedUnsignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(vmask_t<kRatio> vm, V vd, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaaddu_tum(vm, vd, vs2, rs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaaddu_tum(vm, vd, vs2, rs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaaddu_tum(vm, vd, vs2, rs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaaddu_tum(vm, vd, vs2, rs1, __RISCV_VXRM_ROD, vl);
  }
}
};
}  // namespace internal
template <VXRM kVXRM>
constexpr inline internal::vaaddu<kVXRM> vaaddu{};"""
    )


def test_vaaddu_mu():
    c = gen_fixed_h.fixed_arith_op("vaaddu")("mu")
    assert (
        c.cpp_repr
        == """namespace internal {
template <VXRM kVXRM>
  requires SupportedVXRM<kVXRM>
struct vaaddu {
template <typename V, size_t kRatio>
  requires SupportedUnsignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(vmask_t<kRatio> vm, V vd, V vs2, V vs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaaddu_mu(vm, vd, vs2, vs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaaddu_mu(vm, vd, vs2, vs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaaddu_mu(vm, vd, vs2, vs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaaddu_mu(vm, vd, vs2, vs1, __RISCV_VXRM_ROD, vl);
  }
}
template <typename V, size_t kRatio>
  requires SupportedUnsignedVReg<V> && CompatibleVRegRatio<V, kRatio>
RVV_ALWAYS_INLINE
V operator()(vmask_t<kRatio> vm, V vd, V vs2, elem_t<V> rs1, vl_t<kRatio> vl) const {
  if constexpr (kVXRM == VXRM::kRNU) {
    return __riscv_vaaddu_mu(vm, vd, vs2, rs1, __RISCV_VXRM_RNU, vl);
  } else if constexpr (kVXRM == VXRM::kRNE) {
    return __riscv_vaaddu_mu(vm, vd, vs2, rs1, __RISCV_VXRM_RNE, vl);
  } else if constexpr (kVXRM == VXRM::kRDN) {
    return __riscv_vaaddu_mu(vm, vd, vs2, rs1, __RISCV_VXRM_RDN, vl);
  } else if constexpr (kVXRM == VXRM::kROD) {
    return __riscv_vaaddu_mu(vm, vd, vs2, rs1, __RISCV_VXRM_ROD, vl);
  }
}
};
}  // namespace internal
template <VXRM kVXRM>
constexpr inline internal::vaaddu<kVXRM> vaaddu{};"""
    )
