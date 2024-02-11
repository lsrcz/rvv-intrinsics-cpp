// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>
#include <rvv/perm.h>
#include <rvv/policy/mu/perm.h>
#include <rvv/policy/tu/perm.h>
#include <rvv/policy/tumu/perm.h>

#define SLIDE1_TEST(name, ratio, short_name, lmul)                             \
  OP_TEST_ALL(name##_v_##short_name##lmul, name, rvv::vmask_t<ratio>,          \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (C_TYPE_NAME(short_name), rs1), (rvv::vl_t<ratio>, vl))

SLIDE1_TEST(vslide1down, 16, i32, m2);
SLIDE1_TEST(vslide1down, 16, u16, m1);
SLIDE1_TEST(vslide1up, 16, i32, m2);
SLIDE1_TEST(vslide1up, 16, u16, m1);
#if HAS_ZVFH
SLIDE1_TEST(vfslide1down, 16, f16, m1);
SLIDE1_TEST(vfslide1up, 16, f16, m1);
#endif

#if HAS_ZVE32F
SLIDE1_TEST(vfslide1down, 16, f32, m2);
SLIDE1_TEST(vfslide1up, 16, f32, m2);
#endif

#if HAS_ZVE64D
SLIDE1_TEST(vfslide1down, 32, f64, m2);
SLIDE1_TEST(vfslide1up, 32, f64, m2);
#endif
