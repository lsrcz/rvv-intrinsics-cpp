// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define NARROW_OP_TEST(name, ratio, short_name, lmul)                     \
  OP_TEST_ALL(name##_x_x_w_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              VREG_NAME(short_name, lmul),                                \
              (WIDEN_VREG_NAME(short_name, lmul), vs2),                   \
              (rvv::vl_t<ratio>, vl));

NARROW_OP_TEST(vncvt, 8, i8, m1);
NARROW_OP_TEST(vncvt, 8, u8, m1);
