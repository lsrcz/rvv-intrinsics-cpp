// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/perm.h>
#include <rvv/policy/mu/perm.h>
#include <rvv/policy/tu/perm.h>
#include <rvv/policy/tumu/perm.h>

#define SLIDEUP_TEST(name, ratio, short_name, lmul)                           \
  OP_TEST_ALL_NO_DEST(name##_v_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                      VREG_NAME(short_name, lmul),                            \
                      (VREG_NAME(short_name, lmul), vd),                      \
                      (VREG_NAME(short_name, lmul), vs2), (size_t, rs1),      \
                      (rvv::vl_t<ratio>, vl))

SLIDEUP_TEST(vslideup, 16, i32, m2);
SLIDEUP_TEST(vslideup, 16, u16, m1);
#if HAS_ZVFH
SLIDEUP_TEST(vslideup, 16, f16, m1);
#endif

#if HAS_ZVE32F
SLIDEUP_TEST(vslideup, 16, f32, m2);
#endif

#if HAS_ZVE64D
SLIDEUP_TEST(vslideup, 32, f64, m2);
#endif
