// Copyright(c) 2024 < Sirui Lu(siruilu @cs.washington.edu) >
#include <macros.h>
#include <rvv/misc.h>

#define VCREATE_REG_TEST2(short_name, lmul, lmul_large)             \
  VREG_NAME(short_name, lmul_large)                                 \
  vcreate_v_##short_name##lmul##2(VREG_NAME(short_name, lmul) v0,   \
                                  VREG_NAME(short_name, lmul) v1) { \
    return rvv::vcreate<VREG_NAME(short_name, lmul_large)>(v0, v1); \
  }                                                                 \
  static_assert(true, "Require trailing semicolon")

VCREATE_REG_TEST2(i8, m1, m2);
VCREATE_REG_TEST2(u8, m4, m8);
#if HAS_ZVE64X
VCREATE_REG_TEST2(i64, m4, m8);
#endif

#if HAS_ZVFH
VCREATE_REG_TEST2(f64, m4, m8);
#endif
#if HAS_ZVE32F
VCREATE_REG_TEST2(f32, m4, m8);
#endif
#if HAS_ZVE64D
VCREATE_REG_TEST2(f64, m4, m8);
#endif

#define VCREATE_REG_TEST8(short_name, lmul, lmul_large)                        \
  VREG_NAME(short_name, lmul_large)                                            \
  vcreate_v_##short_name##lmul##8(                                             \
      VREG_NAME(short_name, lmul) v0, VREG_NAME(short_name, lmul) v1,          \
      VREG_NAME(short_name, lmul) v2, VREG_NAME(short_name, lmul) v3,          \
      VREG_NAME(short_name, lmul) v4, VREG_NAME(short_name, lmul) v5,          \
      VREG_NAME(short_name, lmul) v6, VREG_NAME(short_name, lmul) v7) {        \
    return rvv::vcreate<VREG_NAME(short_name, lmul_large)>(v0, v1, v2, v3, v4, \
                                                           v5, v6, v7);        \
  }                                                                            \
  static_assert(true, "Require trailing semicolon")

VCREATE_REG_TEST8(i8, m1, m8);
VCREATE_REG_TEST8(u8, m1, m8);
#if HAS_ZVE64X
VCREATE_REG_TEST8(i64, m1, m8);
#endif

#if HAS_ZVFH
VCREATE_REG_TEST8(f64, m1, m8);
#endif
#if HAS_ZVE32F
VCREATE_REG_TEST8(f32, m1, m8);
#endif
#if HAS_ZVE64D
VCREATE_REG_TEST8(f64, m1, m8);
#endif

#if __riscv_v_intrinsic >= 1000000
#define VCREATE_TUPLE_TEST2(short_name, lmul)                           \
  VTUPLE_NAME(short_name, lmul, 2)                                      \
  vcreate_t_##short_name##lmul##index(VREG_NAME(short_name, lmul) v0,   \
                                      VREG_NAME(short_name, lmul) v1) { \
    return rvv::vcreate<VTUPLE_NAME(short_name, lmul, 2)>(v0, v1);      \
  }                                                                     \
  static_assert(true, "Require trailing semicolon")

VCREATE_TUPLE_TEST2(i8, m1);
VCREATE_TUPLE_TEST2(u8, m4);
#if HAS_ZVE64X
VCREATE_TUPLE_TEST2(i64, m4);
#endif

#if HAS_ZVFH
VCREATE_TUPLE_TEST2(f64, m4);
#endif
#if HAS_ZVE32F
VCREATE_TUPLE_TEST2(f32, m4);
#endif
#if HAS_ZVE64D
VCREATE_TUPLE_TEST2(f64, m4);
#endif

#define VCREATE_TUPLE_TEST8(short_name)                                     \
  VTUPLE_NAME(short_name, m1, 8)                                            \
  vcreate_t_##short_name##lmul##index(                                      \
      VREG_NAME(short_name, m1) v0, VREG_NAME(short_name, m1) v1,           \
      VREG_NAME(short_name, m1) v2, VREG_NAME(short_name, m1) v3,           \
      VREG_NAME(short_name, m1) v4, VREG_NAME(short_name, m1) v5,           \
      VREG_NAME(short_name, m1) v6, VREG_NAME(short_name, m1) v7) {         \
    return rvv::vcreate<VTUPLE_NAME(short_name, m1, 8)>(v0, v1, v2, v3, v4, \
                                                        v5, v6, v7);        \
  }                                                                         \
  static_assert(true, "Require trailing semicolon")

VCREATE_TUPLE_TEST8(i8);
VCREATE_TUPLE_TEST8(u8);
#if HAS_ZVE64X
VCREATE_TUPLE_TEST8(i64);
#endif

#if HAS_ZVFH
VCREATE_TUPLE_TEST8(f64);
#endif
#if HAS_ZVE32F
VCREATE_TUPLE_TEST8(f32);
#endif
#if HAS_ZVE64D
VCREATE_TUPLE_TEST8(f64);
#endif
#endif