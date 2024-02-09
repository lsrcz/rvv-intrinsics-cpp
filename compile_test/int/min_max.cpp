// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_BIN_OP_TEST(OP_TEST_ALL, vmin, vmin, 8, i8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vminu, vminu, 16, u16, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vmax, vmax, 4, i8, m2);
BASE_BIN_OP_TEST(OP_TEST_ALL, vmaxu, vmaxu, 4, u8, m2);
