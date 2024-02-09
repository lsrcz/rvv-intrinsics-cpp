// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#ifndef RVV_TYPE_H_
#define RVV_TYPE_H_

#include <riscv_vector.h>
#include <rvv/config.h>
#include <rvv/type_traits.h>

namespace rvv {
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

// Specialization generated.
template <typename T>
struct GetElemType {};

// Specialization generated.
template <typename T>
struct GetRatio {};
}  // namespace internal

template <typename E, size_t kRatio>
  requires CompatibleElemRatio<E, kRatio>
using vreg_t = internal::VReg<E, kRatio>::RegType;

template <size_t kRatio>
  requires SupportedRatio<kRatio>
using vmask_t = internal::VMask<kRatio>::MaskType;

template <typename T>
using elem_t = internal::GetElemType<T>::ElemType;

template <typename T>
constexpr size_t ratio = internal::GetRatio<T>::kRatio;

template <size_t kRatio>
constexpr size_t ratio<vl_t<kRatio>> = kRatio;

template <typename T>
constexpr LMul lmul = elem_ratio_to_lmul<elem_t<T>, ratio<T>>;

template <typename T>
concept IsVReg = requires {
  typename internal::GetElemType<T>::ElemType;
  internal::GetRatio<T>::kRatio;
};

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

template <typename T, bool kNeedZvfh>
concept SupportedFloatingPointVReg =
    IsVReg<T> && SupportedFloatingPointElement<elem_t<T>, kNeedZvfh>;

template <typename T>
concept SupportedIntegral =
    SupportedIntegralVReg<T> || SupportedIntegralElement<T>;

template <typename T>
concept SupportedSigned = SupportedSignedVReg<T> || SupportedSignedElement<T>;

template <typename T>
concept SupportedUnsigned =
    SupportedUnsignedVReg<T> || SupportedUnsignedElement<T>;

template <typename T, bool kNeedZvfh>
concept SupportedFloatingPoint = SupportedFloatingPointVReg<T, kNeedZvfh> ||
                                 SupportedFloatingPointElement<T, kNeedZvfh>;

namespace internal {
template <typename E>
struct WidenedType {};
template <typename E>
struct NarrowedType {};
}  // namespace internal

template <typename T>
using widen_t = typename internal::WidenedType<T>::Type;
template <typename T>
using narrow_t = typename internal::NarrowedType<T>::Type;

template <typename T>
concept Widenable = requires { typename internal::WidenedType<T>::Type; };

template <typename T>
concept Narrowable = requires { typename internal::NarrowedType<T>::Type; };

namespace internal {
template <size_t kN>
struct WidenedNType {};

template <>
struct WidenedNType<2> {
  template <typename T>
    requires Widenable<T>
  using Type = widen_t<T>;
};
template <>
struct WidenedNType<4> {
  template <typename T>
    requires Widenable<T> && Widenable<widen_t<T>>
  using Type = widen_t<widen_t<T>>;
};
template <>
struct WidenedNType<8> {
  template <typename T>
    requires Widenable<T> && Widenable<widen_t<T>> &&
                 Widenable<widen_t<widen_t<T>>>
  using Type = widen_t<widen_t<widen_t<T>>>;
};
}  // namespace internal

template <size_t kN, typename T>
using widen_n_t = typename internal::WidenedNType<kN>::template Type<T>;

template <size_t kN, typename T>
concept WidenableN =
    requires { typename internal::WidenedNType<kN>::template Type<T>; };

namespace internal {
template <typename T>
struct ToUnsigned {
  using Type = T;
};
template <typename T>
  requires SupportedSignedElement<T>
struct ToUnsigned<T> {
  using Type = T;
};
template <typename T>
  requires SupportedSignedVReg<T>
struct ToUnsigned<T> {
  using Type = T;
};
template <typename T>
struct ToSigned {
  using Type = T;
};
template <typename T>
  requires SupportedUnsignedElement<T>
struct ToSigned<T> {
  using Type = T;
};
template <typename T>
  requires SupportedSignedVReg<T>
struct ToSigned<T> {
  using Type = T;
};
}  // namespace internal

template <typename T>
using to_unsigned_t = typename internal::ToUnsigned<T>::Type;

template <typename T>
using to_signed_t = typename internal::ToSigned<T>::Type;

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
