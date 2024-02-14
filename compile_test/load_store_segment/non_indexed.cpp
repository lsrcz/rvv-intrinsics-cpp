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
#define VLSSEG_TEST(ratio, short_name, lmul, tuple_size)                      \
  OP_TEST_ALL(vlsseg_v_##short_name##lmul##x##tuple_size, vlsseg<tuple_size>, \
              rvv::vmask_t<ratio>, VTUPLE_NAME(short_name, lmul, tuple_size), \
              (CONST_PTR(C_TYPE_NAME(short_name)), rs1), (ptrdiff_t, rs2),    \
              (rvv::vl_t<ratio>, vl))                                         \
  static_assert(true, "Require trailing semicolon")
#define VSSEG_TEST(ratio, short_name, lmul, tuple_size)               \
  OP_TEST_NO_POLICY(vsseg_v_##short_name##lmul##x##tuple_size, vsseg, \
                    rvv::vmask_t<ratio>, void,                        \
                    (PTR(C_TYPE_NAME(short_name)), rs1),              \
                    (VTUPLE_NAME(short_name, lmul, tuple_size), vs3), \
                    (rvv::vl_t<ratio>, vl))
#define VSSSEG_TEST(ratio, short_name, lmul, tuple_size)                   \
  OP_TEST_NO_POLICY(vssseg_v_##short_name##lmul##x##tuple_size, vssseg,    \
                    rvv::vmask_t<ratio>, void,                             \
                    (PTR(C_TYPE_NAME(short_name)), rs1), (ptrdiff_t, rs2), \
                    (VTUPLE_NAME(short_name, lmul, tuple_size), vs3),      \
                    (rvv::vl_t<ratio>, vl))
#define NON_INDEXED_TEST(ratio, short_name, lmul, tuple_size) \
  VLSEG_TEST(ratio, short_name, lmul, tuple_size);            \
  VLSSEG_TEST(ratio, short_name, lmul, tuple_size);           \
  VSSEG_TEST(ratio, short_name, lmul, tuple_size);            \
  VSSSEG_TEST(ratio, short_name, lmul, tuple_size);           \
  static_assert(true, "Require trailing semicolon")

NON_INDEXED_TEST(8, i8, m1, 8);
NON_INDEXED_TEST(4, i8, m2, 4);
#if HAS_ZVE64X
NON_INDEXED_TEST(32, u64, m2, 4);
#endif
#if HAS_ZVFH
NON_INDEXED_TEST(8, f16, m2, 4);
#endif
#if HAS_ZVE32F
NON_INDEXED_TEST(8, f32, m4, 2);
#endif
#if HAS_ZVE64D
NON_INDEXED_TEST(32, f64, m2, 3);
#endif
