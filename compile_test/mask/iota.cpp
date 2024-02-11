// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/mask.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/mask.h>
#include <rvv/policy/tu/mask.h>
#include <rvv/policy/tumu/mask.h>

#define IOTA_TEST_SINGLE(name, ratio, short_name, lmul)               \
  OP_TEST(name##_v_##short_name##lmul, name<C_TYPE_NAME(short_name)>, \
          rvv::vmask_t<ratio>, VREG_NAME(short_name, lmul),           \
          (rvv::vmask_t<ratio>, vs2), (rvv::vl_t<ratio>, vl))

IOTA_TEST_SINGLE(viota, 8, u8, m1);
IOTA_TEST_SINGLE(viota, 32, u32, m1);
IOTA_TEST_SINGLE(viota, 16, u32, m2);
