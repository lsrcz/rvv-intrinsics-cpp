// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define SHIFT_OP_TEST(name, ratio, short_name, lmul)                   \
  OP_TEST_ALL(name##_wv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              VREG_NAME(short_name, lmul),                             \
              (WIDEN_VREG_NAME(short_name, lmul), vs2),                \
              (VREG_NAME(TO_UNSIGNED(short_name), lmul), vs1),         \
              (rvv::vl_t<ratio>, vl));                                 \
  OP_TEST_ALL(name##_wx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              VREG_NAME(short_name, lmul),                             \
              (WIDEN_VREG_NAME(short_name, lmul), vs2), (size_t, vs1), \
              (rvv::vl_t<ratio>, vl));

SHIFT_OP_TEST(vnsrl, 8, u32, m4);
SHIFT_OP_TEST(vnsra, 16, i16, m1);
