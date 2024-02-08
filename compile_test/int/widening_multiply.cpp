// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define SU_WIDENING_VV_OP_TEST(name, ratio, short_name, lmul)                \
  OP_TEST_ALL(                                                               \
      name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>,               \
      WIDEN_VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
      (UNSIGNED_VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define SU_WIDENING_VX_OP_TEST(name, ratio, short_name, lmul)                \
  OP_TEST_ALL(                                                               \
      name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,               \
      WIDEN_VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
      (C_TYPE_NAME(TO_UNSIGNED(short_name)), vs1), (rvv::vl_t<ratio>, vl));

WIDENING_VV_OP_TEST(vwmul, 8, i8, m1);
WIDENING_VX_OP_TEST(vwmul, 8, i8, m1);
WIDENING_VV_OP_TEST(vwmulu, 8, u8, m1);
WIDENING_VX_OP_TEST(vwmulu, 8, u8, m1);
SU_WIDENING_VV_OP_TEST(vwmulsu, 8, i16, m2);
SU_WIDENING_VX_OP_TEST(vwmulsu, 8, i16, m2);
