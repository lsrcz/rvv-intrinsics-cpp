// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/load_store_segment.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/load_store_segment.h>
#include <rvv/policy/tu/load_store_segment.h>
#include <rvv/policy/tumu/load_store_segment.h>

#define VLSEG_TEST(ratio, short_name, lmul, tuple_size)                       \
  OP_TEST_ALL(vlseg_v_##short_name##lmul##x##tuple_size, vlseg<tuple_size>,   \
              rvv::vmask_t<ratio>, VTUPLE_NAME(short_name, lmul, tuple_size), \
              (CONST_PTR(C_TYPE_NAME(short_name)), rs1),                      \
              (rvv::vl_t<ratio>, vl))                                         \
  static_assert(true, "Require trailing semicolon")

VLSEG_TEST(8, i8, m1, 8);
VLSEG_TEST(4, i8, m2, 4);
#if HAS_ZVE64X
VLSEG_TEST(32, u64, m2, 4);
#endif
#if HAS_ZVFH
VLSEG_TEST(8, f16, m2, 4);
#endif
#if HAS_ZVE32F
VLSEG_TEST(8, f32, m4, 2);
#endif
#if HAS_ZVE64D
VLSEG_TEST(32, f64, m2, 3);
#endif

#define VLSSEG_TEST(ratio, short_name, lmul, tuple_size)                      \
  OP_TEST_ALL(vlsseg_v_##short_name##lmul##x##tuple_size, vlsseg<tuple_size>, \
              rvv::vmask_t<ratio>, VTUPLE_NAME(short_name, lmul, tuple_size), \
              (CONST_PTR(C_TYPE_NAME(short_name)), rs1), (ptrdiff_t, rs2),    \
              (rvv::vl_t<ratio>, vl))                                         \
  static_assert(true, "Require trailing semicolon")

VLSSEG_TEST(8, i8, m1, 8);
VLSSEG_TEST(4, i8, m2, 4);
#if HAS_ZVE64X
VLSSEG_TEST(32, u64, m2, 4);
#endif
#if HAS_ZVFH
VLSSEG_TEST(8, f16, m2, 4);
#endif
#if HAS_ZVE32F
VLSSEG_TEST(8, f32, m4, 2);
#endif
#if HAS_ZVE64D
VLSSEG_TEST(32, f64, m2, 3);
#endif
