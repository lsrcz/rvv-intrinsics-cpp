// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define VV_OP_TEST(name, ratio, short_name, lmul)                      \
  OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                       \
              (VREG_NAME(short_name, lmul), vs2),                      \
              (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define VX_OP_TEST(name, ratio, short_name, lmul)                      \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                       \
              (VREG_NAME(short_name, lmul), vs2),                      \
              (C_TYPE_NAME(short_name), vs1), (rvv::vl_t<ratio>, vl));
#define WV_OP_TEST(name, ratio, short_name, lmul)                      \
  OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                       \
              (WIDEN_VREG_NAME(short_name, lmul), vs2),                \
              (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define WX_OP_TEST(name, ratio, short_name, lmul)                      \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                       \
              (WIDEN_VREG_NAME(short_name, lmul), vs2),                \
              (C_TYPE_NAME(short_name), vs1), (rvv::vl_t<ratio>, vl));
#define WIDENING_OP_TEST(name, ratio, short_name, lmul) \
  VV_OP_TEST(name, ratio, short_name, lmul)             \
  VX_OP_TEST(name, ratio, short_name, lmul)             \
  WV_OP_TEST(name, ratio, short_name, lmul)             \
  WX_OP_TEST(name, ratio, short_name, lmul)

WIDENING_OP_TEST(vwadd, 8, i8, m1);
WIDENING_OP_TEST(vwsub, 2, i8, m4);
WIDENING_OP_TEST(vwaddu, 8, u8, m1);
WIDENING_OP_TEST(vwsubu, 2, u8, m4);
