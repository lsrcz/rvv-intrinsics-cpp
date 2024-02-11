// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/mask.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/mask.h>
#include <rvv/policy/tu/mask.h>
#include <rvv/policy/tumu/mask.h>

#define MASK_COUNT_UNARY_TEST_SINGLE(name, ratio)                    \
  OP_TEST(name##_m_##ratio, name, rvv::vmask_t<ratio>, unsigned int, \
          (rvv::vmask_t<ratio>, vs), (rvv::vl_t<ratio>, vl))

#define MASK_COUNT_UNARY_TEST(name) \
  NONE_64_MASK_TEST(MASK_COUNT_UNARY_TEST_SINGLE, name)

MASK_COUNT_UNARY_TEST(vcpop);

#if HAS_ELEN64
MASK_COUNT_UNARY_TEST_SINGLE(vcpop, 64);
#endif
