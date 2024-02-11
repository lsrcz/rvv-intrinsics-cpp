// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/reduce.h>
#include <rvv/policy/tu/reduce.h>
#include <rvv/policy/tumu/reduce.h>
#include <rvv/reduce.h>

WIDENING_REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vwredsum, vwredsum, 4,
                           i8, m2);
WIDENING_REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vwredsumu, vwredsumu, 8,
                           u16, m2);
