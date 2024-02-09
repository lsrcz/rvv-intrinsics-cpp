// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

WIDENING_FMA_VV_OP_TEST(vwmacc, 8, i8, m1);
WIDENING_FMA_VX_OP_TEST(vwmacc, 8, i8, m1);
WIDENING_FMA_VV_OP_TEST(vwmaccu, 8, u8, m1);
WIDENING_FMA_VX_OP_TEST(vwmaccu, 8, u8, m1);

#define SU_WIDENING_FMA_VV_OP_TEST(name, ratio, short_name, lmul)          \
  FMA_OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  WIDEN_VREG_NAME(short_name, lmul),                       \
                  (WIDEN_VREG_NAME(short_name, lmul), vd),                 \
                  (VREG_NAME(short_name, lmul), vs1),                      \
                  (UNSIGNED_VREG_NAME(short_name, lmul), vs2),             \
                  (rvv::vl_t<ratio>, vl));

#define SU_WIDENING_FMA_VX_OP_TEST(name, ratio, short_name, lmul)              \
  FMA_OP_TEST_ALL(                                                             \
      name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,                 \
      WIDEN_VREG_NAME(short_name, lmul),                                       \
      (WIDEN_VREG_NAME(short_name, lmul), vd), (C_TYPE_NAME(short_name), rs1), \
      (UNSIGNED_VREG_NAME(short_name, lmul), vs2), (rvv::vl_t<ratio>, vl));

SU_WIDENING_FMA_VV_OP_TEST(vwmaccsu, 8, i8, m1);
SU_WIDENING_FMA_VX_OP_TEST(vwmaccsu, 8, i8, m1);

#define US_WIDENING_FMA_VX_OP_TEST(name, ratio, short_name, lmul)          \
  FMA_OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  WIDEN_VREG_NAME(short_name, lmul),                       \
                  (WIDEN_VREG_NAME(short_name, lmul), vd),                 \
                  (C_TYPE_NAME(TO_UNSIGNED(short_name)), rs1),             \
                  (VREG_NAME(short_name, lmul), vs2), (rvv::vl_t<ratio>, vl));

US_WIDENING_FMA_VX_OP_TEST(vwmaccus, 8, i8, m1);
