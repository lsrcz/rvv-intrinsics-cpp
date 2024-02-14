// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/load_store_segment.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/load_store_segment.h>
#include <rvv/policy/tu/load_store_segment.h>
#include <rvv/policy/tumu/load_store_segment.h>

#define SINGLE_INDEXED_LOAD_TEST(inst, ratio, short_name, lmul, tuple_size,   \
                                 idx_short_name, idx_lmul)                    \
  OP_TEST_ALL(inst##_v_##short_name##lmul##x##tuple_size, inst<tuple_size>,   \
              rvv::vmask_t<ratio>, VTUPLE_NAME(short_name, lmul, tuple_size), \
              (CONST_PTR(C_TYPE_NAME(short_name)), rs1),                      \
              (VREG_NAME(idx_short_name, idx_lmul), rs2),                     \
              (rvv::vl_t<ratio>, vl))                                         \
  static_assert(true, "Require trailing semicolon")
#define SINGLE_INDEXED_STORE_TEST(inst, ratio, short_name, lmul, tuple_size, \
                                  idx_short_name, idx_lmul)                  \
  OP_TEST_NO_POLICY(inst##_v_##short_name##lmul##x##tuple_size, inst,        \
                    rvv::vmask_t<ratio>, void,                               \
                    (PTR(C_TYPE_NAME(short_name)), rs1),                     \
                    (VREG_NAME(idx_short_name, idx_lmul), rs2),              \
                    (VTUPLE_NAME(short_name, lmul, tuple_size), vs3),        \
                    (rvv::vl_t<ratio>, vl))                                  \
  static_assert(true, "Require trailing semicolon")

#define INDEXED_TEST(ratio, short_name, lmul, tuple_size, idx_short_name, \
                     idx_lmul)                                            \
  SINGLE_INDEXED_LOAD_TEST(vloxseg, ratio, short_name, lmul, tuple_size,  \
                           idx_short_name, idx_lmul);                     \
  SINGLE_INDEXED_LOAD_TEST(vluxseg, ratio, short_name, lmul, tuple_size,  \
                           idx_short_name, idx_lmul);                     \
  SINGLE_INDEXED_STORE_TEST(vsoxseg, ratio, short_name, lmul, tuple_size, \
                            idx_short_name, idx_lmul);                    \
  SINGLE_INDEXED_STORE_TEST(vsuxseg, ratio, short_name, lmul, tuple_size, \
                            idx_short_name, idx_lmul);                    \
  static_assert(true, "Require trailing semicolon")

INDEXED_TEST(8, i8, m1, 2, u8, m1);
INDEXED_TEST(8, i8, m1, 8, u8, m1);
INDEXED_TEST(8, i8, m1, 2, u16, m2);
INDEXED_TEST(8, i8, m1, 8, u16, m2);
INDEXED_TEST(4, i8, m2, 2, u16, m4);
INDEXED_TEST(4, i8, m2, 4, u16, m4);
INDEXED_TEST(2, i8, m4, 2, u16, m8);

#if HAS_ZVE64X
INDEXED_TEST(8, i8, m1, 2, u64, m8);
INDEXED_TEST(8, i8, m1, 8, u64, m8);
INDEXED_TEST(16, i64, m4, 2, u8, mf2);
INDEXED_TEST(64, i8, mf8, 8, u64, m1);
#endif
#if HAS_ZVFH
INDEXED_TEST(16, f16, m1, 2, u16, m1);
#endif
#if HAS_ZVE32F
INDEXED_TEST(32, f32, m1, 2, u16, mf2);
#endif
#if HAS_ZVE64D
INDEXED_TEST(16, f64, m4, 2, u16, m1);
#endif
