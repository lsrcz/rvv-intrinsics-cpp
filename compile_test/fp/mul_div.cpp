// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
FP_TEST(BASE_BIN_OP_TEST, OP_TEST_ALL, vfmul, 16, f16, m1);
FP_TEST(BASE_BIN_OP_TEST, OP_TEST_ALL, vfdiv, 8, f16, m2);
FP_TEST(BASE_VX_OP_TEST, OP_TEST_ALL, vfrdiv, 4, f16, m4);
#endif

#if HAS_ZVE32F
FP_TEST(BASE_BIN_OP_TEST, OP_TEST_ALL, vfmul, 32, f32, m1);
FP_TEST(BASE_BIN_OP_TEST, OP_TEST_ALL, vfdiv, 16, f32, m2);
FP_TEST(BASE_VX_OP_TEST, OP_TEST_ALL, vfrdiv, 8, f32, m4);
#endif

#if HAS_ZVE64D
FP_TEST(BASE_BIN_OP_TEST, OP_TEST_ALL, vfmul, 64, f64, m1);
FP_TEST(BASE_BIN_OP_TEST, OP_TEST_ALL, vfdiv, 32, f64, m2);
FP_TEST(BASE_VX_OP_TEST, OP_TEST_ALL, vfrdiv, 16, f64, m4);
#endif
