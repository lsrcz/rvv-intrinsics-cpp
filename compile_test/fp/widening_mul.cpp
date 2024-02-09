// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVE32F && HAS_ZVE64D
FP_TEST(BASE_WIDENING_VV_OP_TEST, OP_TEST_ALL, vfwmul, 8, f32, m4);
FP_TEST(BASE_WIDENING_VX_OP_TEST, OP_TEST_ALL, vfwmul, 16, f32, m2);
#endif

#if HAS_ZVFHMIN && HAS_ZVE32F
FP_TEST(BASE_WIDENING_VV_OP_TEST, OP_TEST_ALL, vfwmul, 4, f16, m4);
FP_TEST(BASE_WIDENING_VX_OP_TEST, OP_TEST_ALL, vfwmul, 8, f16, m2);
#endif
