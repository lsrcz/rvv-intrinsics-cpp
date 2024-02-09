// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_WITH_CARRY_TEST(OP_TEST_NO_MASK, vmerge, vmerge, 2, i16, m8)
BASE_WITH_CARRY_TEST(OP_TEST_NO_MASK, vmerge, vmerge, 8, u16, m2)
