// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
BASE_VVM_V_TEST(OP_TEST_NO_MASK, vmerge, vmerge, 4, f16, m4)
BASE_VXM_V_TEST(OP_TEST_NO_MASK, vfmerge, vfmerge, 4, f16, m4)
#endif

#if HAS_ZVE32F
BASE_VVM_V_TEST(OP_TEST_NO_MASK, vmerge, vmerge, 8, f32, m4)
BASE_VXM_V_TEST(OP_TEST_NO_MASK, vfmerge, vfmerge, 8, f32, m4)
#endif

#if HAS_ZVE64D
BASE_VVM_V_TEST(OP_TEST_NO_MASK, vmerge, vmerge, 8, f64, m8)
BASE_VXM_V_TEST(OP_TEST_NO_MASK, vfmerge, vfmerge, 8, f64, m8)
#endif
