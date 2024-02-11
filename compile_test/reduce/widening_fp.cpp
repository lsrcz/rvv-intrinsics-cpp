// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/reduce.h>
#include <rvv/policy/tu/reduce.h>
#include <rvv/policy/tumu/reduce.h>
#include <rvv/reduce.h>

#if HAS_ZVFH && HAS_ZVE32F
WIDENING_REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfwredosum, vfwredosum,
                           4, f16, m4);
WIDENING_REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfwredusum, vfwredusum,
                           8, f16, m2);
#endif

#if HAS_ZVE32F && HAS_ZVE64D
WIDENING_REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfwredosum, vfwredosum,
                           8, f32, m4);
WIDENING_REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfwredusum, vfwredusum,
                           16, f32, m2);
#endif
