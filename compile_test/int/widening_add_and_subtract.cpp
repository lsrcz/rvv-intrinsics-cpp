// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

WIDENING_OP_TEST(vwadd, 8, i8, m1);
WIDENING_OP_TEST(vwsub, 2, i8, m4);
WIDENING_OP_TEST(vwaddu, 8, u8, m1);
WIDENING_OP_TEST(vwsubu, 2, u8, m4);
