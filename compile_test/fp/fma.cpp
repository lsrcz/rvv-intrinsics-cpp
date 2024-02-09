// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#if HAS_ZVFH
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmacc, vfmacc, 8, f16, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmacc, vfnmacc, 8, f16, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmadd, vfmadd, 8, f16, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmadd, vfnmadd, 8, f16, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmsac, vfmsac, 8, f16, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmsac, vfnmsac, 8, f16, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmsub, vfmsub, 8, f16, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmsub, vfnmsub, 8, f16, m2);
#endif

#if HAS_ZVE32F
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmacc, vfmacc, 16, f32, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmacc, vfnmacc, 16, f32, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmadd, vfmadd, 16, f32, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmadd, vfnmadd, 16, f32, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmsac, vfmsac, 16, f32, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmsac, vfnmsac, 16, f32, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmsub, vfmsub, 16, f32, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmsub, vfnmsub, 16, f32, m2);
#endif

#if HAS_ZVE64D
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmacc, vfmacc, 32, f64, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmacc, vfnmacc, 32, f64, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmadd, vfmadd, 32, f64, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmadd, vfnmadd, 32, f64, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmsac, vfmsac, 32, f64, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmsac, vfnmsac, 32, f64, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfmsub, vfmsub, 32, f64, m2);
BASE_FMA_OP_TEST(OP_TEST_ALL_NO_DEST, vfnmsub, vfnmsub, 32, f64, m2);
#endif
