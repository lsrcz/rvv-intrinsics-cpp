// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define WIDENING_TEST(name, ratio, short_name, lmul)                      \
  OP_TEST_ALL(name##_x_x_v_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                          \
              (VREG_NAME(short_name, lmul), vs2), (rvv::vl_t<ratio>, vl));

WIDENING_TEST(vwcvt, 8, i8, m1);
WIDENING_TEST(vwcvtu, 16, u16, m1);
