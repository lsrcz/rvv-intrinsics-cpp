// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_BIN_OP_TEST(OP_TEST_ALL, vand, vand, 8, i8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vor, vor, 4, u8, m2);
BASE_BIN_OP_TEST(OP_TEST_ALL, vxor, vxor, 16, u32, m2);
BASE_UNARY_OP_TEST(OP_TEST_ALL, vnot, vnot, 8, i8, m1);
