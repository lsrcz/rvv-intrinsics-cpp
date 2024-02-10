// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#if HAS_ZVFH
BASE_UNARY_OP_TEST(OP_TEST_NO_MASK, vmv, vmv, 16, f16, m1);
#endif

#if HAS_ZVE32F
BASE_UNARY_OP_TEST(OP_TEST_NO_MASK, vmv, vmv, 32, f32, m1);
#endif

#if HAS_ZVE64D
BASE_UNARY_OP_TEST(OP_TEST_NO_MASK, vmv, vmv, 32, f64, m2);
#endif
