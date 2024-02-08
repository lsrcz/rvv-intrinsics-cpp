// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BIN_OP_TEST(vand, 8, i8, m1);
BIN_OP_TEST(vor, 4, u8, m2);
BIN_OP_TEST(vxor, 16, u32, m2);
UNARY_OP_TEST(vnot, 8, i8, m1);
