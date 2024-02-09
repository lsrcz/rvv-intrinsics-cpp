// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmseq, vmseq, 8, i8, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmseq, vmseq, 16, u16, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsne, vmsne, 8, i8, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsne, vmsne, 16, u16, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmslt, vmslt, 8, i8, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsltu, vmsltu, 8, u8, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsle, vmsle, 16, i32, m2);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsleu, vmsleu, 16, u32, m2);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsgt, vmsgt, 32, i32, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsgtu, vmsgtu, 32, u32, m1);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsge, vmsge, 16, i32, m2);
BASE_COMPARE_OP_TEST(OP_TEST_NO_TAIL, vmsgeu, vmsgeu, 16, u32, m2);
