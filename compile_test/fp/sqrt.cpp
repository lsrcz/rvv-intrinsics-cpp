// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
FP_TEST(BASE_UNARY_OP_TEST, OP_TEST_ALL, vfsqrt, 16, f16, m1);
#endif

#if HAS_ZVE32F
FP_TEST(BASE_UNARY_OP_TEST, OP_TEST_ALL, vfsqrt, 32, f32, m1);
#endif

#if HAS_ZVE64D
FP_TEST(BASE_UNARY_OP_TEST, OP_TEST_ALL, vfsqrt, 64, f64, m1);
#endif
