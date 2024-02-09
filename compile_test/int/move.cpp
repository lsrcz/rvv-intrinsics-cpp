// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_UNARY_OP_TEST(OP_TEST_NO_MASK, vmv, vmv, 16, i16, m1);
BASE_UNARY_OP_TEST(OP_TEST_NO_MASK, vmv, vmv, 32, u32, m1);
