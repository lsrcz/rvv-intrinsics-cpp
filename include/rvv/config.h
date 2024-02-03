// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#ifndef RVV_CONFIG_H_
#define RVV_CONFIG_H_

#define RVV_CONFIG_H_
#define RVV_ALWAYS_INLINE inline __attribute__((always_inline))
#define RVV_ALWAYS_INLINE_CONSTEXPR constexpr RVV_ALWAYS_INLINE

namespace rvv {
#if defined(__STDCPP_FLOAT16_T__)
#define HAVE_FLOAT16 1
using float16_t = std::float16_t;
#elif defined(__FLT16_MAX__)
#define HAVE_FLOAT16 1
using float16_t = decltype(__FLT16_MAX__);
#else
#define HAVE_FLOAT16 0
using float16_t = void;
#endif

using float32_t = float;

using float64_t = double;
};  // namespace rvv

#endif  // RVV_CONFIG_H_
