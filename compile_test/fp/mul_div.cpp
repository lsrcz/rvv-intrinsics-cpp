// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
BIN_OP_TEST(vfmul, 16, f16, m1);
BIN_OP_TEST(vfdiv, 8, f16, m2);
VX_OP_TEST(vfrdiv, 4, f16, m4);
#endif

#if HAS_ZVE32F
BIN_OP_TEST(vfmul, 32, f32, m1);
BIN_OP_TEST(vfdiv, 16, f32, m2);
VX_OP_TEST(vfrdiv, 8, f32, m4);
#endif

#if HAS_ZVE64D
BIN_OP_TEST(vfmul, 64, f64, m1);
BIN_OP_TEST(vfdiv, 32, f64, m2);
VX_OP_TEST(vfrdiv, 16, f64, m4);
#endif
