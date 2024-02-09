// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define SU_VV_OP_TEST(name, ratio, short_name, lmul)                           \
  OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (UNSIGNED_VREG_NAME(short_name, lmul), vs1),                     \
              (rvv::vl_t<ratio>, vl));

#define SU_VX_OP_TEST(name, ratio, short_name, lmul)                           \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (C_TYPE_NAME(TO_UNSIGNED(short_name)), rs1),                     \
              (rvv::vl_t<ratio>, vl));

#define SU_OP_TEST(name, ratio, short_name, lmul) \
  SU_VV_OP_TEST(name, ratio, short_name, lmul)    \
  SU_VX_OP_TEST(name, ratio, short_name, lmul)

BASE_BIN_OP_TEST(OP_TEST_ALL, vmul, vmul, 8, i8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vmul, vmul, 16, u16, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vmulh, vmulh, 4, i8, m2);
BASE_BIN_OP_TEST(OP_TEST_ALL, vmulhu, vmulhu, 16, u32, m2);
SU_OP_TEST(vmulhsu, 4, i16, m4);
