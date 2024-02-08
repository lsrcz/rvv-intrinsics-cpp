// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fixed.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fixed.h>
#include <rvv/policy/tu/fixed.h>
#include <rvv/policy/tumu/fixed.h>

BIN_OP_TEST(vsadd, 8, i8, m1);
BIN_OP_TEST(vsaddu, 16, u8, mf2);
BIN_OP_TEST(vssub, 1, i8, m8);
BIN_OP_TEST(vssubu, 4, u8, m2);
