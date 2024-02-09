// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#if HAS_ZVFH && HAS_ZVE32F
WIDENING_FMA_VV_OP_TEST(vfwmacc, 16, f16, m1);
WIDENING_FMA_VX_OP_TEST(vfwnmacc, 16, f16, m1);
WIDENING_FMA_VV_OP_TEST(vfwmsac, 16, f16, m1);
WIDENING_FMA_VX_OP_TEST(vfwnmsac, 16, f16, m1);
#endif

#if HAS_ZVE32F && HAS_ZVE64D
WIDENING_FMA_VV_OP_TEST(vfwmacc, 32, f32, m1);
WIDENING_FMA_VX_OP_TEST(vfwnmacc, 32, f32, m1);
WIDENING_FMA_VV_OP_TEST(vfwmsac, 32, f32, m1);
WIDENING_FMA_VX_OP_TEST(vfwnmsac, 32, f32, m1);
#endif
