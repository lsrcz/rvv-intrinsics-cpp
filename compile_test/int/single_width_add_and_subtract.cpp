// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BIN_OP_TEST(vadd, 8, i8, m1);
BIN_OP_TEST(vsub, 4, u8, m2);
VX_OP_TEST(vrsub, 4, i16, m4);
UNARY_OP_TEST(vneg, 16, i8, mf2);
