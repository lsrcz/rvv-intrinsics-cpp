// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/perm.h>
#include <rvv/policy/mu/perm.h>
#include <rvv/policy/tu/perm.h>
#include <rvv/policy/tumu/perm.h>

#define VREG_TO_SCALAR_MOVE_TEST(name, ratio, short_name, lmul)   \
  OP_TEST(name##_v_##short_name##lmul, name, rvv::vmask_t<ratio>, \
          C_TYPE_NAME(short_name), (VREG_NAME(short_name, lmul), vs))

#if HAS_ZVFH
BASE_SCALAR_TO_VECTOR_MOVE_OP_TEST(OP_TEST_NO_MASK, vfmv_s, vfmv_s, 8, f16, m2)
VREG_TO_SCALAR_MOVE_TEST(vfmv_f, 8, f16, m2)
#endif

#if HAS_ZVE32F
BASE_SCALAR_TO_VECTOR_MOVE_OP_TEST(OP_TEST_NO_MASK, vfmv_s, vfmv_s, 16, f32, m2)
VREG_TO_SCALAR_MOVE_TEST(vfmv_f, 16, f32, m2)
#endif

#if HAS_ZVE64D
BASE_SCALAR_TO_VECTOR_MOVE_OP_TEST(OP_TEST_NO_MASK, vfmv_s, vfmv_s, 32, f64, m2)
VREG_TO_SCALAR_MOVE_TEST(vfmv_f, 32, f64, m2)
#endif

BASE_SCALAR_TO_VECTOR_MOVE_OP_TEST(OP_TEST_NO_MASK, vmv_s, vmv_s, 16, i32, m2)
VREG_TO_SCALAR_MOVE_TEST(vmv_x, 16, i32, m2)
