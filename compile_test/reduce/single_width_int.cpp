// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/reduce.h>
#include <rvv/policy/tu/reduce.h>
#include <rvv/policy/tumu/reduce.h>
#include <rvv/reduce.h>

REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredsum, vredsum, 8, i8, m1);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredsum, vredsum, 8, u16, m2);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredand, vredand, 2, i8, m4);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredand, vredand, 2, u16, m8);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredor, vredor, 16, i8, mf2);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredor, vredor, 32, u16, mf2);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredxor, vredxor, 8, i8, m1);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredxor, vredxor, 8, u16, m2);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredmin, vredmin, 2, i8, m4);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredminu, vredminu, 2, u16, m8);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredmax, vredmax, 16, i8, mf2);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vredmaxu, vredmaxu, 32, u16,
                  mf2);
