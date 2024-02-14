// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>

#define VUNDEFINED_TEST(short_name, lmul)                         \
  VREG_NAME(short_name, lmul) vundefined_v_##short_name##lmul() { \
    return rvv::vundefined<VREG_NAME(short_name, lmul)>();        \
  }                                                               \
  static_assert(true, "Require trailing semicolon")

VUNDEFINED_TEST(i8, m1);
VUNDEFINED_TEST(u16, mf2);
VUNDEFINED_TEST(u32, m1);

#if HAS_ZVE64X
VUNDEFINED_TEST(u64, m1);
#endif

#if HAS_ZVFH
VUNDEFINED_TEST(f16, m4);
#endif

#if HAS_ZVE32F
VUNDEFINED_TEST(f32, m2);
#endif

#if HAS_ZVE64D
VUNDEFINED_TEST(f64, m4);
#endif