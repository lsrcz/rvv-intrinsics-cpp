// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/perm.h>
#include <rvv/policy/mu/perm.h>
#include <rvv/policy/tu/perm.h>
#include <rvv/policy/tumu/perm.h>

#define VRGATHER_TEST_V_EI16(name, ratio, short_name, lmul, lmul_ei16)         \
  OP_TEST_ALL(name##_v_ei16_##short_name##lmul, name, rvv::vmask_t<ratio>,     \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (VREG_NAME(u16, lmul_ei16), vs1), (rvv::vl_t<ratio>, vl));
#define VRGATHER_TEST_VV(name, ratio, short_name, lmul)                        \
  OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (VREG_NAME(TO_UNSIGNED(short_name), lmul), vs1),                 \
              (rvv::vl_t<ratio>, vl));
#define VRGATHER_TEST_VX(name, ratio, short_name, lmul)                        \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (size_t, vs1), (rvv::vl_t<ratio>, vl))
#define VRGATHER_TEST(name, ratio, short_name, lmul, lmul_ei16)   \
  VRGATHER_TEST_V_EI16(name, ratio, short_name, lmul, lmul_ei16); \
  VRGATHER_TEST_VV(name, ratio, short_name, lmul);                \
  VRGATHER_TEST_VX(name, ratio, short_name, lmul);

#if HAS_ZVFH
VRGATHER_TEST(vrgather, 16, f16, m1, m1);
#endif

#if HAS_ZVE32F
VRGATHER_TEST(vrgather, 16, f32, m2, m1);
#endif

#if HAS_ZVE64D
VRGATHER_TEST(vrgather, 32, f64, m2, mf2);
#endif

VRGATHER_TEST(vrgather, 16, i32, m2, m1);
VRGATHER_TEST(vrgather, 16, u16, m1, m1);
