// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#if HAS_ZVFH
FMA_OP_TEST(vfmacc, 8, f16, m2);
FMA_OP_TEST(vfnmacc, 8, f16, m2);
FMA_OP_TEST(vfmadd, 8, f16, m2);
FMA_OP_TEST(vfnmadd, 8, f16, m2);
FMA_OP_TEST(vfmsac, 8, f16, m2);
FMA_OP_TEST(vfnmsac, 8, f16, m2);
FMA_OP_TEST(vfmsub, 8, f16, m2);
FMA_OP_TEST(vfnmsub, 8, f16, m2);
#endif

#if HAS_ZVE32F
FMA_OP_TEST(vfmacc, 16, f32, m2);
FMA_OP_TEST(vfnmacc, 16, f32, m2);
FMA_OP_TEST(vfmadd, 16, f32, m2);
FMA_OP_TEST(vfnmadd, 16, f32, m2);
FMA_OP_TEST(vfmsac, 16, f32, m2);
FMA_OP_TEST(vfnmsac, 16, f32, m2);
FMA_OP_TEST(vfmsub, 16, f32, m2);
FMA_OP_TEST(vfnmsub, 16, f32, m2);
#endif

#if HAS_ZVE64D
FMA_OP_TEST(vfmacc, 32, f64, m2);
FMA_OP_TEST(vfnmacc, 32, f64, m2);
FMA_OP_TEST(vfmadd, 32, f64, m2);
FMA_OP_TEST(vfnmadd, 32, f64, m2);
FMA_OP_TEST(vfmsac, 32, f64, m2);
FMA_OP_TEST(vfnmsac, 32, f64, m2);
FMA_OP_TEST(vfmsub, 32, f64, m2);
FMA_OP_TEST(vfnmsub, 32, f64, m2);
#endif
