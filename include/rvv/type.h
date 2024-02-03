// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#ifndef RVV_TYPE_H_
#define RVV_TYPE_H_

#include <riscv_vector.h>
#include <rvv/config.h>

#include "rvv/type_traits.h"

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

template <typename E, size_t kRatio>
  requires is_supported_rvv_elem_type<E, false> && is_supported_ratio<kRatio>
constexpr LMul lmul =
    static_cast<LMul>(internal::log2(static_cast<int>(sizeof(E))) -
                      internal::log2(static_cast<int>(kRatio)) + 3);

template <typename E, size_t kRatio>
concept is_compatible_elem_ratio =
    is_supported_rvv_elem_type<E, false> && is_supported_ratio<kRatio> &&
    lmul<E, kRatio> >= LMul::kMF8 && lmul<E, kRatio> <= LMul::kM8;

template <size_t kRatio_>
  requires is_supported_ratio<kRatio_>
struct vl_t {
  size_t vl;
  RVV_ALWAYS_INLINE_CONSTEXPR operator size_t() const { return vl; }
};

namespace internal {
template <typename E, size_t kRatio>
  requires is_compatible_elem_ratio<E, kRatio>
struct VReg {};

template <size_t kRatio>
  requires is_supported_ratio<kRatio>
struct VMask {};

template <typename T>
struct GetElemType {};

template <typename T>
struct GetRatio {};
}  // namespace internal

template <typename E, size_t kRatio>
  requires is_compatible_elem_ratio<E, kRatio>
using vreg_t = internal::VReg<E, kRatio>::type;

template <size_t kRatio>
  requires is_supported_ratio<kRatio>
using vmask_t = internal::VMask<kRatio>::type;

template <typename T>
using elem_t = internal::GetElemType<T>::ElemType;

template <typename T>
constexpr size_t ratio_v = internal::GetRatio<T>::kRatio;

}  // namespace rvv

#endif  // RVV_TYPE_H_
