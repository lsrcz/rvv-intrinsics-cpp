// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#include "macros/op_test_base.h"

BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vmadd, vmadd, 4, i8, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vnmsub, vnmsub, 8, i8, m1);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vmadd, vmadd, 16, u16, m1);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vnmsac, vnmsac, 32, u16, mf2);
