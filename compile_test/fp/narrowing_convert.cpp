// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fp.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fp.h>
#include <rvv/policy/tu/fp.h>
#include <rvv/policy/tumu/fp.h>

#if HAS_ZVE32F
CVT_OP_TEST(NARROW_SIGNED_VREG_NAME, vfncvt_x, 8, f32, m4);
CVT_OP_TEST(NARROW_SIGNED_VREG_NAME, vfncvt_rtz_x, 8, f32, m4);
CVT_OP_TEST(NARROW_UNSIGNED_VREG_NAME, vfncvt_xu, 8, f32, m4);
CVT_OP_TEST(NARROW_UNSIGNED_VREG_NAME, vfncvt_rtz_xu, 8, f32, m4);
#endif

#if HAS_ZVFH
CVT_OP_TEST(NARROW_FP_VREG_NAME, vfncvt_f, 8, i32, m4);
CVT_OP_TEST(NARROW_FP_VREG_NAME, vfncvt_f, 8, u32, m4);
#endif

#if HAS_ZVFHMIN
CVT_OP_TEST(NARROW_FP_VREG_NAME, vfncvt_f, 8, f32, m4);
#endif

#if HAS_ZVE64D
CVT_OP_TEST(NARROW_SIGNED_VREG_NAME, vfncvt_x, 16, f64, m4);
CVT_OP_TEST(NARROW_SIGNED_VREG_NAME, vfncvt_rtz_x, 16, f64, m4);
CVT_OP_TEST(NARROW_UNSIGNED_VREG_NAME, vfncvt_xu, 16, f64, m4);
CVT_OP_TEST(NARROW_UNSIGNED_VREG_NAME, vfncvt_rtz_xu, 16, f64, m4);
#endif

#if HAS_ZVE32F
#if HAS_ZVE64X
CVT_OP_TEST(NARROW_FP_VREG_NAME, vfncvt_f, 16, i64, m4);
CVT_OP_TEST(NARROW_FP_VREG_NAME, vfncvt_f, 16, u64, m4);
#endif
#if HAS_ZVE64D
CVT_OP_TEST(NARROW_FP_VREG_NAME, vfncvt_f, 16, f64, m4);
#endif
#endif
