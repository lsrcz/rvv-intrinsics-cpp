// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BIN_OP_TEST(vmin, 8, i8, m1);
BIN_OP_TEST(vminu, 16, u16, m1);
BIN_OP_TEST(vmax, 4, i8, m2);
BIN_OP_TEST(vmaxu, 4, u8, m2);
