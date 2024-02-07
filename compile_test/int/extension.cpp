// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define EXTENSION_TEST(name, n, ratio, short_name, lmul)                    \
  OP_TEST_ALL(name##_vf##n##_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME_N(n, short_name, lmul),                       \
              (VREG_NAME(short_name, lmul), vs2), (rvv::vl_t<ratio>, vl));

EXTENSION_TEST(vsext2, 2, 8, i8, m1);
EXTENSION_TEST(vsext4, 4, 8, i8, m1);
EXTENSION_TEST(vzext2, 2, 8, u8, m1);
EXTENSION_TEST(vzext4, 4, 8, u8, m1);
#if HAS_ZVE64X
EXTENSION_TEST(vsext8, 8, 8, i8, m1);
EXTENSION_TEST(vzext8, 8, 8, u8, m1);
#endif
