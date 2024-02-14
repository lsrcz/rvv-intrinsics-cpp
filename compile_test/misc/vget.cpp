// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>

#define VGET_REG_TEST(short_name, lmul, index, lmul_large)                \
  VREG_NAME(short_name, lmul)                                             \
  vget_v_##short_name##lmul##index(VREG_NAME(short_name, lmul_large) a) { \
    return rvv::vget<VREG_NAME(short_name, lmul), index>(a);              \
  }                                                                       \
  static_assert(true, "Require trailing semicolon")

#define VGET_REG_TEST_ALL(short_name)   \
  VGET_REG_TEST(short_name, m1, 0, m2); \
  VGET_REG_TEST(short_name, m1, 1, m2); \
  VGET_REG_TEST(short_name, m1, 0, m8); \
  VGET_REG_TEST(short_name, m1, 7, m8); \
  VGET_REG_TEST(short_name, m2, 0, m4); \
  VGET_REG_TEST(short_name, m2, 1, m4); \
  VGET_REG_TEST(short_name, m2, 0, m8); \
  VGET_REG_TEST(short_name, m2, 3, m8); \
  VGET_REG_TEST(short_name, m4, 0, m8); \
  VGET_REG_TEST(short_name, m4, 1, m8);

VGET_REG_TEST_ALL(i8);
VGET_REG_TEST_ALL(u8);
VGET_REG_TEST_ALL(i16);
VGET_REG_TEST_ALL(u16);
VGET_REG_TEST_ALL(i32);
VGET_REG_TEST_ALL(u32);

#if HAS_ZVE64X
VGET_REG_TEST_ALL(i64);
VGET_REG_TEST_ALL(u64);
#endif

#if HAS_ZVFH
VGET_REG_TEST_ALL(f16);
#endif

#if HAS_ZVE32F
VGET_REG_TEST_ALL(f32);
#endif

#if HAS_ZVE64D
VGET_REG_TEST_ALL(f64);
#endif

#define VGET_TUPLE_TEST(short_name, lmul, tuple_size, index) \
  VREG_NAME(short_name, lmul)                                \
  vget_t_##short_name##tuple_size##index(                    \
      VTUPLE_NAME(short_name, lmul, tuple_size) a) {         \
    return rvv::vget<VREG_NAME(short_name, lmul), index>(a); \
  }                                                          \
  static_assert(true, "Require trailing semicolon")

#if HAS_ELEN64
VGET_TUPLE_TEST(i8, mf8, 8, 0);
VGET_TUPLE_TEST(i8, mf8, 8, 7);
#endif
VGET_TUPLE_TEST(i8, mf4, 6, 0);
VGET_TUPLE_TEST(i8, mf4, 6, 5);
VGET_TUPLE_TEST(i8, mf4, 2, 0);
VGET_TUPLE_TEST(i8, mf4, 2, 1);
VGET_TUPLE_TEST(i8, m1, 4, 3);
VGET_TUPLE_TEST(i8, m4, 2, 1);
VGET_TUPLE_TEST(u8, m1, 4, 3);
VGET_TUPLE_TEST(u32, m1, 4, 3);

#if HAS_ZVE64X
VGET_TUPLE_TEST(u64, m1, 4, 3);
VGET_TUPLE_TEST(u64, m4, 2, 0);
#endif

#if HAS_ZVFH
VGET_TUPLE_TEST(f16, mf2, 4, 3);
VGET_TUPLE_TEST(f16, m4, 2, 0);
#endif

#if HAS_ZVE32F
#if HAS_ELEN64
VGET_TUPLE_TEST(f32, mf2, 8, 3);
#endif
VGET_TUPLE_TEST(f32, m1, 4, 3);
VGET_TUPLE_TEST(f32, m4, 2, 0);
#endif

#if HAS_ZVE64D
#if HAS_ELEN64
VGET_TUPLE_TEST(f64, m1, 4, 3);
#endif
VGET_TUPLE_TEST(f64, m4, 2, 0);
#endif

#define VLMUL_TRUNC_REG_TEST(short_name, lmul, lmul_large)                  \
  VREG_NAME(short_name, lmul)                                               \
  vlmul_trunc_v_##short_name##lmul##index(VREG_NAME(short_name, lmul_large) \
                                              a) {                          \
    return rvv::vlmul_trunc<VREG_NAME(short_name, lmul)>(a);                \
  }                                                                         \
  static_assert(true, "Require trailing semicolon")

#define VLMUL_TRUNC_TEST_ALL(short_name)    \
  VLMUL_TRUNC_REG_TEST(short_name, m1, m2); \
  VLMUL_TRUNC_REG_TEST(short_name, m1, m4); \
  VLMUL_TRUNC_REG_TEST(short_name, m1, m8); \
  VLMUL_TRUNC_REG_TEST(short_name, m2, m4); \
  VLMUL_TRUNC_REG_TEST(short_name, m2, m8); \
  VLMUL_TRUNC_REG_TEST(short_name, m4, m8); \
  static_assert(true, "Require trailing semicolon")

VLMUL_TRUNC_TEST_ALL(i8);
VLMUL_TRUNC_TEST_ALL(u8);
VLMUL_TRUNC_TEST_ALL(i16);
VLMUL_TRUNC_TEST_ALL(u16);
VLMUL_TRUNC_TEST_ALL(i32);
VLMUL_TRUNC_TEST_ALL(u32);

#if HAS_ZVE64X
VLMUL_TRUNC_TEST_ALL(i64);
VLMUL_TRUNC_TEST_ALL(u64);
#endif

#if HAS_ZVFH
VLMUL_TRUNC_TEST_ALL(f16);
#endif

#if HAS_ZVE32F
VLMUL_TRUNC_TEST_ALL(f32);
#endif

#if HAS_ZVE64D
VLMUL_TRUNC_TEST_ALL(f64);
#endif
