// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#include "macros/op_test_base.h"

#if HAS_ZVFH && HAS_ZVE32F
FP_TEST(BASE_WIDENING_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfwmsac, 16, f16, m1);
FP_TEST(BASE_WIDENING_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfwnmsac, 16, f16, m1);
#endif

#if HAS_ZVE32F && HAS_ZVE64D
FP_TEST(BASE_WIDENING_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfwmsac, 32, f32, m1);
FP_TEST(BASE_WIDENING_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfwnmsac, 32, f32, m1);
#endif
