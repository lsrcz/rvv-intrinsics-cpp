// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_WIDENING_OP_TEST(OP_TEST_ALL, vwadd, vwadd, 8, i8, m1);
BASE_WIDENING_OP_TEST(OP_TEST_ALL, vwsub, vwsub, 2, i8, m4);
BASE_WIDENING_OP_TEST(OP_TEST_ALL, vwaddu, vwaddu, 8, u8, m1);
BASE_WIDENING_OP_TEST(OP_TEST_ALL, vwsubu, vwsubu, 2, u8, m4);
