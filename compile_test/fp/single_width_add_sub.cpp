// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
BIN_OP_TEST(vfadd, 16, f16, m1);
BIN_OP_TEST(vfsub, 8, f16, m2);
VX_OP_TEST(vfrsub, 4, f16, m4);
UNARY_OP_TEST(vfneg, 8, f16, m2);
#endif

BIN_OP_TEST(vfadd, 32, f32, m1);
BIN_OP_TEST(vfsub, 16, f32, m2);
VX_OP_TEST(vfrsub, 8, f32, m4);
UNARY_OP_TEST(vfneg, 16, f32, m2);

#if HAS_ZVE64D
BIN_OP_TEST(vfadd, 64, f64, m1);
BIN_OP_TEST(vfsub, 32, f64, m2);
VX_OP_TEST(vfrsub, 16, f64, m4);
UNARY_OP_TEST(vfneg, 32, f64, m2);
#endif
