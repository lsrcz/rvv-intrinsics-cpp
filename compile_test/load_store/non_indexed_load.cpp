// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/load_store_segment.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/load_store_segment.h>
#include <rvv/policy/tu/load_store_segment.h>
#include <rvv/policy/tumu/load_store_segment.h>

#define VLE_TEST(ratio, short_name, lmul)                         \
  OP_TEST_ALL(vle_v_##short_name##lmul, vle, rvv::vmask_t<ratio>, \
              VREG_NAME(short_name, lmul),                        \
              (CONST_PTR(C_TYPE_NAME(short_name)), rs1),          \
              (rvv::vl_t<ratio>, vl))                             \
  static_assert(true, "Require trailing semicolon")
#define VLSE_TEST(ratio, short_name, lmul)                                 \
  OP_TEST_ALL(vlse_v_##short_name##lmul, vlse, rvv::vmask_t<ratio>,        \
              VREG_NAME(short_name, lmul),                                 \
              (CONST_PTR(C_TYPE_NAME(short_name)), rs1), (ptrdiff_t, rs2), \
              (rvv::vl_t<ratio>, vl))                                      \
  static_assert(true, "Require trailing semicolon")
#define NON_INDEXED_TEST(ratio, short_name, lmul) \
  VLE_TEST(ratio, short_name, lmul);              \
  VLSE_TEST(ratio, short_name, lmul);             \
  static_assert(true, "Require trailing semicolon")

NON_INDEXED_TEST(8, i8, m1);
NON_INDEXED_TEST(4, i8, m2);
#if HAS_ZVE64X
NON_INDEXED_TEST(32, u64, m2);
#endif
#if HAS_ZVFH
NON_INDEXED_TEST(8, f16, m2);
#endif
#if HAS_ZVE32F
NON_INDEXED_TEST(8, f32, m4);
#endif
#if HAS_ZVE64D
NON_INDEXED_TEST(32, f64, m2);
#endif
