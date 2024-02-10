// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
CVT_OP_TEST(SIGNED_VREG_NAME, vfcvt_x, 8, f16, m2);
CVT_OP_TEST(SIGNED_VREG_NAME, vfcvt_rtz_x, 8, f16, m2);
CVT_OP_TEST(UNSIGNED_VREG_NAME, vfcvt_xu, 8, f16, m2);
CVT_OP_TEST(UNSIGNED_VREG_NAME, vfcvt_rtz_xu, 8, f16, m2);
CVT_OP_TEST(FP_VREG_NAME, vfcvt_f, 8, i16, m2);
CVT_OP_TEST(FP_VREG_NAME, vfcvt_f, 8, u16, m2);
#endif

#if HAS_ZVE32F
CVT_OP_TEST(SIGNED_VREG_NAME, vfcvt_x, 16, f32, m2);
CVT_OP_TEST(SIGNED_VREG_NAME, vfcvt_rtz_x, 16, f32, m2);
CVT_OP_TEST(UNSIGNED_VREG_NAME, vfcvt_xu, 16, f32, m2);
CVT_OP_TEST(UNSIGNED_VREG_NAME, vfcvt_rtz_xu, 16, f32, m2);
CVT_OP_TEST(FP_VREG_NAME, vfcvt_f, 16, i32, m2);
CVT_OP_TEST(FP_VREG_NAME, vfcvt_f, 16, u32, m2);
#endif

#if HAS_ZVE64D
CVT_OP_TEST(SIGNED_VREG_NAME, vfcvt_x, 32, f64, m2);
CVT_OP_TEST(SIGNED_VREG_NAME, vfcvt_rtz_x, 32, f64, m2);
CVT_OP_TEST(UNSIGNED_VREG_NAME, vfcvt_xu, 32, f64, m2);
CVT_OP_TEST(UNSIGNED_VREG_NAME, vfcvt_rtz_xu, 32, f64, m2);
CVT_OP_TEST(FP_VREG_NAME, vfcvt_f, 32, i64, m2);
CVT_OP_TEST(FP_VREG_NAME, vfcvt_f, 32, u64, m2);
#endif
