// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVE32F && HAS_ZVE64D
BASE_WIDENING_OP_TEST(OP_TEST_ALL, vfwadd, vfwadd, 8, f32, m4);
BASE_WIDENING_OP_TEST(OP_TEST_ALL, vfwsub, vfwsub, 16, f32, m2);
#endif

#if HAS_ZVFHMIN && HAS_ZVE32F
BASE_WIDENING_OP_TEST(OP_TEST_ALL, vfwadd, vfwadd, 4, f16, m4);
BASE_WIDENING_OP_TEST(OP_TEST_ALL, vfwsub, vfwsub, 8, f16, m2);
#endif
