// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_MOVE_OP_TEST(OP_TEST_NO_MASK, vmv_v, vmv_v, 16, i16, m1);
BASE_MOVE_OP_TEST(OP_TEST_NO_MASK, vmv_v, vmv_v, 32, u32, m1);
