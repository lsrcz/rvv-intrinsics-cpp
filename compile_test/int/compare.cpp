// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define COMPARE_VV_OP_TEST(name, ratio, short_name, lmul)                  \
  OP_TEST_NO_TAIL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2), \
                  (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));

#define COMPARE_VX_OP_TEST(name, ratio, short_name, lmul)                  \
  OP_TEST_NO_TAIL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2), \
                  (C_TYPE_NAME(short_name), rs1), (rvv::vl_t<ratio>, vl));

#define COMPARE_OP_TEST(name, ratio, short_name, lmul) \
  COMPARE_VV_OP_TEST(name, ratio, short_name, lmul)    \
  COMPARE_VX_OP_TEST(name, ratio, short_name, lmul)

COMPARE_OP_TEST(vmseq, 8, i8, m1);
COMPARE_OP_TEST(vmseq, 16, u16, m1);
COMPARE_OP_TEST(vmsne, 8, i8, m1);
COMPARE_OP_TEST(vmsne, 16, u16, m1);
COMPARE_OP_TEST(vmslt, 8, i8, m1);
COMPARE_OP_TEST(vmsltu, 8, u8, m1);
COMPARE_OP_TEST(vmsle, 16, i32, m2);
COMPARE_OP_TEST(vmsleu, 16, u32, m2);
COMPARE_OP_TEST(vmsgt, 32, i32, m1);
COMPARE_OP_TEST(vmsgtu, 32, u32, m1);
COMPARE_OP_TEST(vmsge, 16, i32, m2);
COMPARE_OP_TEST(vmsgeu, 16, u32, m2);
