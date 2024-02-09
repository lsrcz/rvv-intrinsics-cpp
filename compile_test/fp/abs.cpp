// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
BASE_UNARY_OP_TEST(OP_TEST_ALL, vfabs, vfabs, 8, f16, m2);
#endif

#if HAS_ZVE32F
BASE_UNARY_OP_TEST(OP_TEST_ALL, vfabs, vfabs, 16, f32, m2);
#endif

#if HAS_ZVE64D
BASE_UNARY_OP_TEST(OP_TEST_ALL, vfabs, vfabs, 32, f64, m2);
#endif
