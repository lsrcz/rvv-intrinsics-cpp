// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/reduce.h>
#include <rvv/policy/tu/reduce.h>
#include <rvv/policy/tumu/reduce.h>
#include <rvv/reduce.h>

#if HAS_ZVFH
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredosum, vfredosum, 8, f16,
                  m2);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredusum, vfredusum, 32, f16,
                  mf2);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredmin, vfredmin, 4, f16, m4);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredmax, vfredmax, 2, f16, m8);
#endif

#if HAS_ZVE32F
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredosum, vfredosum, 8, f32,
                  m4);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredusum, vfredusum, 32, f32,
                  m1);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredmin, vfredmin, 4, f32, m8);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredmax, vfredmax, 16, f32, m2);
#endif

#if HAS_ZVE64D
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredosum, vfredosum, 16, f64,
                  m4);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredusum, vfredusum, 32, f64,
                  m2);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredmin, vfredmin, 8, f64, m8);
REDUCE_VV_OP_TEST(OP_TEST_NO_MASK_UNDISTURBED, vfredmax, vfredmax, 32, f64, m2);
#endif
