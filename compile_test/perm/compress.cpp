// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/perm.h>
#include <rvv/policy/mu/perm.h>
#include <rvv/policy/tu/perm.h>
#include <rvv/policy/tumu/perm.h>

#define VCOMPRESS_TEST(name, ratio, short_name, lmul)                      \
  OP_TEST_NO_MASK(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  VREG_NAME(short_name, lmul),                             \
                  (VREG_NAME(short_name, lmul), vs2),                      \
                  (rvv::vmask_t<ratio>, vs1), (rvv::vl_t<ratio>, vl));
#if HAS_ZVFH
VCOMPRESS_TEST(vcompress, 16, f16, m1);
#endif

#if HAS_ZVE32F
VCOMPRESS_TEST(vcompress, 16, f32, m2);
#endif

#if HAS_ZVE64D
VCOMPRESS_TEST(vcompress, 32, f64, m2);
#endif

VCOMPRESS_TEST(vcompress, 16, i32, m2);
VCOMPRESS_TEST(vcompress, 16, u16, m1);
