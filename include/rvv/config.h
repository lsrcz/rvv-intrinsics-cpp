// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#ifndef RVV_CONFIG_H_
#define RVV_CONFIG_H_

#define RVV_CONFIG_H_
#define RVV_ALWAYS_INLINE inline __attribute__((always_inline))
#define RVV_ALWAYS_INLINE_CONSTEXPR constexpr RVV_ALWAYS_INLINE

namespace rvv {
#if defined(__STDCPP_FLOAT16_T__)
#define HAS_FLOAT16 1
using float16_t = std::float16_t;
#elif defined(__FLT16_MAX__)
#define HAS_FLOAT16 1
using float16_t = decltype(__FLT16_MAX__);
#else
#define HAS_FLOAT16 0
using float16_t = void;
#endif

using float32_t = float;

using float64_t = double;

#if defined(__riscv_zvfh)
#define HAS_ZVFH 1
#else
#define HAS_ZVFH 0
#endif

#if defined(__riscv_zvfhmin) || defined(__riscv_zvfh)
#define HAS_ZVFHMIN 1
#else
#define HAS_ZVFHMIN 0
#endif

#define RVV_ELEN __riscv_v_elen

#if defined(__riscv_zve32f)
#define HAS_ZVE32F 1
#else
#define HAS_ZVE32F 0
#endif

#if defined(__riscv_zve64d)
#define HAS_ZVE64D 1
#else
#define HAS_ZVE64D 0
#endif

#if defined(__riscv_zve64x)
#define HAS_ZVE64X 1
#else
#define HAS_ZVE64X 0
#endif

#if RVV_ELEN == 64
#define HAS_ELEN64 1
#elif RVV_ELEN == 32
#define HAS_ELEN64 0
#else
#error Unsupported ELEN, currently only 32 and 64 are supported.
#endif

};  // namespace rvv

#endif  // RVV_CONFIG_H_
