// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#if HAS_ZVFH
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmacc, 8, f16, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmacc, 8, f16, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmadd, 8, f16, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmadd, 8, f16, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmsac, 8, f16, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmsac, 8, f16, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmsub, 8, f16, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmsub, 8, f16, m2);
#endif

#if HAS_ZVE32F
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmacc, 16, f32, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmacc, 16, f32, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmadd, 16, f32, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmadd, 16, f32, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmsac, 16, f32, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmsac, 16, f32, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmsub, 16, f32, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmsub, 16, f32, m2);
#endif

#if HAS_ZVE64D
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmacc, 32, f64, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmacc, 32, f64, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmadd, 32, f64, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmadd, 32, f64, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmsac, 32, f64, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmsac, 32, f64, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfmsub, 32, f64, m2);
FP_TEST(BASE_FMA_OP_TEST, OP_TEST_ALL_NO_DEST, vfnmsub, 32, f64, m2);
#endif
