// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVFH
CVT_OP_TEST(WIDEN_SIGNED_VREG_NAME, vfwcvt_x, 8, f16, m2);
CVT_OP_TEST(WIDEN_SIGNED_VREG_NAME, vfwcvt_rtz_x, 8, f16, m2);
CVT_OP_TEST(WIDEN_UNSIGNED_VREG_NAME, vfwcvt_xu, 8, f16, m2);
CVT_OP_TEST(WIDEN_UNSIGNED_VREG_NAME, vfwcvt_rtz_xu, 8, f16, m2);
CVT_OP_TEST(WIDEN_FP_VREG_NAME, vfwcvt_f, 8, i16, m2);
CVT_OP_TEST(WIDEN_FP_VREG_NAME, vfwcvt_f, 8, u16, m2);
#endif

#if HAS_ZVFHMIN
CVT_OP_TEST(WIDEN_FP_VREG_NAME, vfwcvt_f, 8, f16, m2);
#endif

#if HAS_ZVE32F
CVT_OP_TEST(WIDEN_SIGNED_VREG_NAME, vfwcvt_x, 16, f32, m2);
CVT_OP_TEST(WIDEN_SIGNED_VREG_NAME, vfwcvt_rtz_x, 16, f32, m2);
CVT_OP_TEST(WIDEN_UNSIGNED_VREG_NAME, vfwcvt_xu, 16, f32, m2);
CVT_OP_TEST(WIDEN_UNSIGNED_VREG_NAME, vfwcvt_rtz_xu, 16, f32, m2);
CVT_OP_TEST(WIDEN_FP_VREG_NAME, vfwcvt_f, 16, i32, m2);
CVT_OP_TEST(WIDEN_FP_VREG_NAME, vfwcvt_f, 16, u32, m2);
CVT_OP_TEST(WIDEN_FP_VREG_NAME, vfwcvt_f, 16, f32, m2);
#endif
