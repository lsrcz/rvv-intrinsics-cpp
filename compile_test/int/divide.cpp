// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BIN_OP_TEST(vdiv, 8, i8, m1);
BIN_OP_TEST(vdivu, 8, u16, m2);
BIN_OP_TEST(vrem, 8, i8, m1);
BIN_OP_TEST(vremu, 8, u16, m2);
