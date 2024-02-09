// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfeq, vmfeq, 16, f16, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfne, vmfne, 16, f16, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmflt, vmflt, 16, f16, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfle, vmfle, 16, f16, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfgt, vmfgt, 16, f16, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfge, vmfge, 16, f16, m1);
#endif

#if HAS_ZVE32F
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfeq, vmfeq, 32, f32, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfne, vmfne, 32, f32, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmflt, vmflt, 32, f32, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfle, vmfle, 32, f32, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfgt, vmfgt, 32, f32, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfge, vmfge, 32, f32, m1);
#endif

#if HAS_ZVE64D
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfeq, vmfeq, 64, f64, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfne, vmfne, 64, f64, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmflt, vmflt, 64, f64, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfle, vmfle, 64, f64, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfgt, vmfgt, 64, f64, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmfge, vmfge, 64, f64, m1);
#endif
