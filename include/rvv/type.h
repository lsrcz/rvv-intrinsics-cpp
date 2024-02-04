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
concept is_supported_lmul = kLMul >= LMul::kMF8 && kLMul <= LMul::kM8;

template <typename E, size_t kRatio>
  requires is_supported_rvv_elem_type<E, false> && is_supported_ratio<kRatio>
constexpr LMul elem_ratio_to_lmul =
    static_cast<LMul>(internal::log2(static_cast<int>(sizeof(E))) -
                      internal::log2(static_cast<int>(kRatio)) + 3);

template <typename E, size_t kRatio>
concept is_compatible_elem_ratio =
    is_supported_rvv_elem_type<E, false> && is_supported_ratio<kRatio> &&
    is_supported_lmul<elem_ratio_to_lmul<E, kRatio>>;

template <typename E, LMul kLMul>
  requires is_supported_rvv_elem_type<E, false> && is_supported_lmul<kLMul>
constexpr size_t elem_lmul_to_ratio =
    sizeof(E) * (1 << (3 - static_cast<int>(kLMul)));

template <typename E, LMul kLMul>
concept is_compatible_elem_lmul =
    is_supported_rvv_elem_type<E, false> && is_supported_lmul<kLMul> &&
    is_supported_ratio<elem_lmul_to_ratio<E, kLMul>>;

template <size_t kRatio_>
  requires is_supported_ratio<kRatio_>
struct vl_t {
  size_t vl;
  RVV_ALWAYS_INLINE_CONSTEXPR operator size_t() const { return vl; }
};

namespace internal {
// Specialization generated.
template <typename E, size_t kRatio>
  requires is_compatible_elem_ratio<E, kRatio>
struct VReg {};

// Specialization generated.
template <size_t kRatio>
  requires is_supported_ratio<kRatio>
struct VMask {};

// Specialization generated.
template <typename T>
struct GetElemType {};

// Specialization generated.
template <typename T>
struct GetRatio {};
}  // namespace internal

template <typename E, size_t kRatio>
  requires is_compatible_elem_ratio<E, kRatio>
using vreg_t = internal::VReg<E, kRatio>::RegType;

template <size_t kRatio>
  requires is_supported_ratio<kRatio>
using vmask_t = internal::VMask<kRatio>::MaskType;

template <typename T>
using elem_t = internal::GetElemType<T>::ElemType;

template <typename T>
constexpr size_t ratio = internal::GetRatio<T>::kRatio;

template <size_t kRatio>
constexpr size_t ratio<vl_t<kRatio>> = kRatio;

template <typename T>
constexpr LMul lmul = elem_ratio_to_lmul<elem_t<T>, ratio<T>>;

}  // namespace rvv

#include <rvv/type.inc>

#endif  // RVV_TYPE_H_
