// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
BASE_BIN_OP_TEST(OP_TEST_ALL, vfmul, vfmul, 16, f16, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfdiv, vfdiv, 8, f16, m2);
BASE_VX_OP_TEST(OP_TEST_ALL, vfrdiv, vfrdiv, 4, f16, m4);
#endif

#if HAS_ZVE32F
BASE_BIN_OP_TEST(OP_TEST_ALL, vfmul, vfmul, 32, f32, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfdiv, vfdiv, 16, f32, m2);
BASE_VX_OP_TEST(OP_TEST_ALL, vfrdiv, vfrdiv, 8, f32, m4);
#endif

#if HAS_ZVE64D
BASE_BIN_OP_TEST(OP_TEST_ALL, vfmul, vfmul, 64, f64, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfdiv, vfdiv, 32, f64, m2);
BASE_VX_OP_TEST(OP_TEST_ALL, vfrdiv, vfrdiv, 16, f64, m4);
#endif
