// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_WITH_CARRY_TEST(OP_TEST_NO_MASK, vadc, vadc, 2, i16, m8)
BASE_WITH_CARRY_TEST(OP_TEST_NO_MASK, vsbc, vsbc, 8, u16, m2)

#define CARRY_OUT_VX_TEST(name, ratio, short_name, lmul)           \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
          rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2), \
          (C_TYPE_NAME(short_name), vs1), (rvv::vl_t<ratio>, vl));
#define CARRY_OUT_VV_TEST(name, ratio, short_name, lmul)           \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
          rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2), \
          (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define CARRY_OUT_VXM_TEST(name, ratio, short_name, lmul)            \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,   \
          rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2),   \
          (C_TYPE_NAME(short_name), vs1), (rvv::vmask_t<ratio>, v0), \
          (rvv::vl_t<ratio>, vl));
#define CARRY_OUT_VVM_TEST(name, ratio, short_name, lmul)                \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,       \
          rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2),       \
          (VREG_NAME(short_name, lmul), vs1), (rvv::vmask_t<ratio>, v0), \
          (rvv::vl_t<ratio>, vl));
#define CARRY_OUT_TEST(name, ratio, short_name, lmul) \
  CARRY_OUT_VX_TEST(name, ratio, short_name, lmul)    \
  CARRY_OUT_VV_TEST(name, ratio, short_name, lmul)    \
  CARRY_OUT_VXM_TEST(name, ratio, short_name, lmul)   \
  CARRY_OUT_VVM_TEST(name, ratio, short_name, lmul)

CARRY_OUT_TEST(vmadc, 2, i16, m8)
CARRY_OUT_TEST(vmsbc, 2, i16, m8)
