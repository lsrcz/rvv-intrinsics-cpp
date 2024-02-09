// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnj, vfsgnj, 16, f16, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnjn, vfsgnjn, 16, f16, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnjx, vfsgnjx, 16, f16, m1);
#endif

#if HAS_ZVE32F
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnj, vfsgnj, 32, f32, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnjn, vfsgnjn, 32, f32, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnjx, vfsgnjx, 32, f32, m1);
#endif

#if HAS_ZVE64D
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnj, vfsgnj, 64, f64, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnjn, vfsgnjn, 64, f64, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vfsgnjx, vfsgnjx, 64, f64, m1);
#endif
