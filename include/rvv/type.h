// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#ifndef RVV_TYPE_H_
#define RVV_TYPE_H_

#include <riscv_vector.h>
#include <rvv/config.h>
#include <rvv/elem.h>

namespace rvv {

// Ratio of SEW and LMUL.
template <size_t kRatio>
concept NeedUnsupportedElen64 = kRatio == 64 && !HAS_ELEN64;

template <size_t kRatio>
concept SupportedRatio =
    (kRatio == 1 || kRatio == 2 || kRatio == 4 || kRatio == 8 || kRatio == 16 ||
     kRatio == 32 || kRatio == 64) &&
    !NeedUnsupportedElen64<kRatio>;

enum class LMul {
  kM8 = 3,
  kM4 = 2,
  kM2 = 1,
  kM1 = 0,
  kMF2 = -1,
  kMF4 = -2,
  kMF8 = -3,
};

namespace internal {
constexpr int log2(int i) {
  int r = 0;
  while (i > 1) {
    i /= 2;
    r++;
  }
  return r;
}

}  // namespace internal

template <LMul kLMul>
concept SupportedLMul = kLMul >= LMul::kMF8 && kLMul <= LMul::kM8;

template <typename E, size_t kRatio>
  requires SupportedElement<E, false> && SupportedRatio<kRatio>
constexpr LMul elem_ratio_to_lmul =
    static_cast<LMul>(internal::log2(static_cast<int>(sizeof(E))) -
                      internal::log2(static_cast<int>(kRatio)) + 3);

template <typename E, size_t kRatio>
concept CompatibleElemRatio =
    SupportedElement<E, false> && SupportedRatio<kRatio> &&
    SupportedLMul<elem_ratio_to_lmul<E, kRatio>>;

template <typename E, LMul kLMul>
  requires SupportedElement<E, false> && SupportedLMul<kLMul>
constexpr size_t elem_lmul_to_ratio =
    sizeof(E) * (1 << (3 - static_cast<int>(kLMul)));

template <typename E, LMul kLMul>
concept CompatibleElemLMul =
    SupportedElement<E, false> && SupportedLMul<kLMul> &&
    SupportedRatio<elem_lmul_to_ratio<E, kLMul>>;

template <size_t kRatio_>
  requires SupportedRatio<kRatio_>
struct vl_t {
  size_t vl;
  RVV_ALWAYS_INLINE_CONSTEXPR operator size_t() const { return vl; }
};

namespace internal {
// Specialization generated.
template <typename E, size_t kRatio>
  requires CompatibleElemRatio<E, kRatio>
struct VReg {};

// Specialization generated.
template <size_t kRatio>
  requires SupportedRatio<kRatio>
struct VMask {};

template <typename V>
struct VRegTraits;

template <typename V>
struct VMaskTraits;

template <typename V>
struct VLTraits;

template <size_t kRatio_>
struct VLTraits<vl_t<kRatio_>> {
  static constexpr size_t kRatio = kRatio_;
};
}  // namespace internal

template <typename T>
concept IsVReg = requires {
  typename internal::VRegTraits<T>::ElemType;
  internal::VRegTraits<T>::kRatio;
};

template <typename T>
concept IsVMask = requires { internal::VMaskTraits<T>::kRatio; };

template <typename T>
concept IsVL = requires { internal::VLTraits<T>::kRatio; };

template <typename E, size_t kRatio>
  requires CompatibleElemRatio<E, kRatio>
using vreg_t = internal::VReg<E, kRatio>::RegType;

template <size_t kRatio>
  requires SupportedRatio<kRatio>
using vmask_t = internal::VMask<kRatio>::MaskType;

namespace internal {
template <typename T>
  requires IsVReg<T> || IsVMask<T> || IsVL<T>
struct GetRatio;
template <typename V>
  requires IsVReg<V>
struct GetRatio<V> {
  static constexpr size_t kRatio = VRegTraits<V>::kRatio;
};
template <typename V>
  requires IsVMask<V>
struct GetRatio<V> {
  static constexpr size_t kRatio = VMaskTraits<V>::kRatio;
};
template <typename V>
  requires IsVL<V>
struct GetRatio<V> {
  static constexpr size_t kRatio = VLTraits<V>::kRatio;
};
}  // namespace internal

template <typename T>
using elem_t = internal::VRegTraits<T>::ElemType;

template <typename T>
constexpr size_t ratio = internal::GetRatio<T>::kRatio;

template <size_t kRatio>
constexpr size_t ratio<vl_t<kRatio>> = kRatio;

template <typename T>
constexpr LMul lmul = elem_ratio_to_lmul<elem_t<T>, ratio<T>>;

template <typename T, size_t kRatio>
concept CompatibleVRegRatio =
    IsVReg<T> && ratio<T> == kRatio && CompatibleElemRatio<elem_t<T>, kRatio>;

template <typename T>
concept SupportedIntegralVReg =
    IsVReg<T> && SupportedIntegralElement<elem_t<T>>;

template <typename T>
concept SupportedSignedVReg = IsVReg<T> && SupportedSignedElement<elem_t<T>>;

template <typename T>
concept SupportedUnsignedVReg =
    IsVReg<T> && SupportedUnsignedElement<elem_t<T>>;

template <typename T, bool kNeedZvfh = true>
concept SupportedFloatingPointVReg =
    IsVReg<T> && SupportedFloatingPointElement<elem_t<T>, kNeedZvfh>;

template <typename T, bool kNeedZvfh = true>
concept SupportedVReg =
    SupportedIntegralVReg<T> || SupportedFloatingPointVReg<T, kNeedZvfh>;

template <typename V>
  requires IsVReg<V>
using vreg_m1_t = vreg_t<elem_t<V>, sizeof(elem_t<V>) * 8>;

enum class VXRM {
  kRNU = 0,
  kRNE = 1,
  kRDN = 2,
  kROD = 3,
};

template <VXRM kVXRM>
concept SupportedVXRM = kVXRM >= VXRM::kRNU && kVXRM <= VXRM::kROD;

enum class FRM {
  kImplicit = 0,
  kRNE = 1,
  kRTZ = 2,
  kRDN = 3,
  kRUP = 4,
  kRMM = 5,
};
template <FRM kFRM>
concept SupportedFRM = kFRM >= FRM::kImplicit && kFRM <= FRM::kRMM;

}  // namespace rvv

#include <rvv/type.inc>

#endif  // RVV_TYPE_H_
