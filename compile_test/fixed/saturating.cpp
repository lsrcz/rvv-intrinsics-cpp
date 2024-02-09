// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fixed.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fixed.h>
#include <rvv/policy/tu/fixed.h>
#include <rvv/policy/tumu/fixed.h>

BASE_BIN_OP_TEST(OP_TEST_ALL, vsadd, vsadd, 8, i8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vsaddu, vsaddu, 16, u8, mf2);
BASE_BIN_OP_TEST(OP_TEST_ALL, vssub, vssub, 1, i8, m8);
BASE_BIN_OP_TEST(OP_TEST_ALL, vssubu, vssubu, 4, u8, m2);
