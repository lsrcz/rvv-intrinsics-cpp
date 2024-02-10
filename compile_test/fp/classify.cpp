// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#define CLASSIFY_OP_TEST(name, ratio, short_name, lmul)               \
  OP_TEST_ALL(name##_v_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              UNSIGNED_VREG_NAME(short_name, lmul),                   \
              (VREG_NAME(short_name, lmul), vs2), (rvv::vl_t<ratio>, vl))

#if HAS_ZVFH
CLASSIFY_OP_TEST(vfclass, 8, f16, m2);
#endif

#if HAS_ZVE32F
CLASSIFY_OP_TEST(vfclass, 16, f32, m2);
#endif

#if HAS_ZVE32F
CLASSIFY_OP_TEST(vfclass, 32, f64, m2);
#endif
