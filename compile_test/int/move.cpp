// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

UNARY_OP_TEST_NO_MASK(vmv, 16, i16, m1);
UNARY_OP_TEST_NO_MASK(vmv, 32, u32, m1);
