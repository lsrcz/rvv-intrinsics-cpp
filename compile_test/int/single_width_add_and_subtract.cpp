// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_BIN_OP_TEST(OP_TEST_ALL, vadd, vadd, 8, i8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vsub, vsub, 4, u8, m2);
BASE_VX_OP_TEST(OP_TEST_ALL, vrsub, vrsub, 4, i16, m4);
BASE_UNARY_OP_TEST(OP_TEST_ALL, vneg, vneg, 16, i8, mf2);
