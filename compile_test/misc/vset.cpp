// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>

#define VSET_REG_TEST(short_name, lmul, index, lmul_large)                 \
  VREG_NAME(short_name, lmul_large)                                        \
  vget_v_##short_name##lmul##index(VREG_NAME(short_name, lmul_large) dest, \
                                   VREG_NAME(short_name, lmul) value) {    \
    return rvv::vset<index>(dest, value);                                  \
  }                                                                        \
  static_assert(true, "Require trailing semicolon")

#define VSET_REG_TEST_ALL(short_name)   \
  VSET_REG_TEST(short_name, m1, 0, m2); \
  VSET_REG_TEST(short_name, m1, 1, m2); \
  VSET_REG_TEST(short_name, m1, 0, m8); \
  VSET_REG_TEST(short_name, m1, 7, m8); \
  VSET_REG_TEST(short_name, m2, 0, m4); \
  VSET_REG_TEST(short_name, m2, 1, m4); \
  VSET_REG_TEST(short_name, m2, 0, m8); \
  VSET_REG_TEST(short_name, m2, 3, m8); \
  VSET_REG_TEST(short_name, m4, 0, m8); \
  VSET_REG_TEST(short_name, m4, 1, m8);

VSET_REG_TEST_ALL(i8);
VSET_REG_TEST_ALL(u8);
VSET_REG_TEST_ALL(i16);
VSET_REG_TEST_ALL(u16);
VSET_REG_TEST_ALL(i32);
VSET_REG_TEST_ALL(u32);

#if HAS_ZVE64X
VSET_REG_TEST_ALL(i64);
VSET_REG_TEST_ALL(u64);
#endif

#if HAS_ZVFH
VSET_REG_TEST_ALL(f16);
#endif

#if HAS_ZVE32F
VSET_REG_TEST_ALL(f32);
#endif

#if HAS_ZVE64D
VSET_REG_TEST_ALL(f64);
#endif

#define VSET_TUPLE_TEST(short_name, lmul, tuple_size, index)                \
  VTUPLE_NAME(short_name, lmul, tuple_size)                                 \
  vset__##short_name##lmul##index(VTUPLE_NAME(short_name, lmul, tuple_size) \
                                      dest,                                 \
                                  VREG_NAME(short_name, lmul) value) {      \
    return rvv::vset<index>(dest, value);                                   \
  }                                                                         \
  static_assert(true, "Require trailing semicolon")

#if HAS_ELEN64
VSET_TUPLE_TEST(i8, mf8, 8, 0);
VSET_TUPLE_TEST(i8, mf8, 8, 7);
#endif
VSET_TUPLE_TEST(i8, mf4, 6, 0);
VSET_TUPLE_TEST(i8, mf4, 6, 5);
VSET_TUPLE_TEST(i8, mf4, 2, 0);
VSET_TUPLE_TEST(i8, mf4, 2, 1);
VSET_TUPLE_TEST(i8, m1, 4, 3);
VSET_TUPLE_TEST(i8, m4, 2, 1);
VSET_TUPLE_TEST(u8, m1, 4, 3);
VSET_TUPLE_TEST(u32, m1, 4, 3);

#if HAS_ZVE64X
VSET_TUPLE_TEST(u64, m1, 4, 3);
VSET_TUPLE_TEST(u64, m4, 2, 0);
#endif

#if HAS_ZVFH
VSET_TUPLE_TEST(f16, mf2, 4, 3);
VSET_TUPLE_TEST(f16, m4, 2, 0);
#endif

#define VLMUL_EXT_REG_TEST(short_name, lmul, lmul_large)                   \
  VREG_NAME(short_name, lmul_large)                                        \
  vlext_trunc_v_##short_name##lmul##lmul_large(VREG_NAME(short_name, lmul) a) { \
    return rvv::vlmul_ext<VREG_NAME(short_name, lmul_large)>(a);           \
  }                                                                        \
  static_assert(true, "Require trailing semicolon")

#define VLMUL_EXT_TEST_ALL(short_name)    \
  VLMUL_EXT_REG_TEST(short_name, m1, m2); \
  VLMUL_EXT_REG_TEST(short_name, m1, m4); \
  VLMUL_EXT_REG_TEST(short_name, m1, m8); \
  VLMUL_EXT_REG_TEST(short_name, m2, m4); \
  VLMUL_EXT_REG_TEST(short_name, m2, m8); \
  VLMUL_EXT_REG_TEST(short_name, m4, m8); \
  static_assert(true, "Require trailing semicolon")

VLMUL_EXT_TEST_ALL(i8);
VLMUL_EXT_TEST_ALL(u8);
VLMUL_EXT_TEST_ALL(i16);
VLMUL_EXT_TEST_ALL(u16);
VLMUL_EXT_TEST_ALL(i32);
VLMUL_EXT_TEST_ALL(u32);

#if HAS_ZVE64X
VLMUL_EXT_TEST_ALL(i64);
VLMUL_EXT_TEST_ALL(u64);
#endif

#if HAS_ZVFH
VLMUL_EXT_TEST_ALL(f16);
#endif

#if HAS_ZVE32F
VLMUL_EXT_TEST_ALL(f32);
#endif

#if HAS_ZVE64D
VLMUL_EXT_TEST_ALL(f64);
#endif
