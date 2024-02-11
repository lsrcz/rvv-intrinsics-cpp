// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/mask.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/mask.h>
#include <rvv/policy/tu/mask.h>
#include <rvv/policy/tumu/mask.h>

#define MASK_SET_TEST_SINGLE(name, ratio)                         \
  OP_TEST_NO_TAIL(name##_m_##ratio, name, rvv::vmask_t<ratio>,    \
                  rvv::vmask_t<ratio>, (rvv::vmask_t<ratio>, vs), \
                  (rvv::vl_t<ratio>, vl))

#define MASK_SET_TEST(name) NONE_64_MASK_TEST(MASK_SET_TEST_SINGLE, name)

MASK_SET_TEST(vmsbf);
MASK_SET_TEST(vmsif);
MASK_SET_TEST(vmsof);

#if HAS_ELEN64
MASK_SET_TEST_SINGLE(vmsbf, 64);
MASK_SET_TEST_SINGLE(vmsif, 64);
MASK_SET_TEST_SINGLE(vmsof, 64);
#endif
