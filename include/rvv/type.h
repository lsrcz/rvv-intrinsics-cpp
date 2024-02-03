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

template <size_t kRatio_>
  requires is_supported_ratio<kRatio_>
struct vl_t {
  size_t vl;
  RVV_ALWAYS_INLINE_CONSTEXPR operator size_t() const { return vl; }
};

namespace internal {
template <typename E, size_t kRatio>
  requires is_supported_rvv_elem_type<E, false> && is_supported_ratio<kRatio>
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
  requires is_supported_rvv_elem_type<E, false> && is_supported_ratio<kRatio>
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
