// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_BIN_OP_TEST(OP_TEST_ALL, vdiv, vdiv, 8, i8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vdivu, vdivu, 8, u16, m2);
BASE_BIN_OP_TEST(OP_TEST_ALL, vrem, vrem, 8, i8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vremu, vremu, 8, u16, m2);
