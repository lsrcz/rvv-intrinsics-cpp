// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define VV_OP_TEST(name, ratio, short_name, lmul)                              \
  OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));

#define VX_OP_TEST(name, ratio, short_name, lmul)                              \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (C_TYPE_NAME(short_name), rs1), (rvv::vl_t<ratio>, vl));

#define BIN_OP_TEST(name, ratio, short_name, lmul) \
  VV_OP_TEST(name, ratio, short_name, lmul)        \
  VX_OP_TEST(name, ratio, short_name, lmul)

#define UNARY_OP_TEST(name, ratio, short_name, lmul)                       \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
          VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
          (rvv::vl_t<ratio>, vl));

BIN_OP_TEST(vadd, 8, i8, m1);
BIN_OP_TEST(vsub, 4, u8, m2);
VX_OP_TEST(vrsub, 4, i16, m4);
UNARY_OP_TEST(vneg, 16, i8, mf2);
