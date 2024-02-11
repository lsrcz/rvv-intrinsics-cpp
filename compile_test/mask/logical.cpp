// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/mask.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/mask.h>
#include <rvv/policy/tu/mask.h>
#include <rvv/policy/tumu/mask.h>

#define MASK_LOGICAL_NULLARY_TEST_SINGLE(name, ratio)                       \
  OP_TEST(name##_m_##ratio, name, rvv::vmask_t<ratio>, rvv::vmask_t<ratio>, \
          (rvv::vl_t<ratio>, vl))

#define MASK_LOGICAL_NULLARY_TEST(name) \
  NONE_64_MASK_TEST(MASK_LOGICAL_NULLARY_TEST_SINGLE, name)

#define MASK_LOGICAL_UNARY_TEST_SINGLE(name, ratio)                         \
  OP_TEST(name##_m_##ratio, name, rvv::vmask_t<ratio>, rvv::vmask_t<ratio>, \
          (rvv::vmask_t<ratio>, vs), (rvv::vl_t<ratio>, vl))

#define MASK_LOGICAL_UNARY_TEST(name) \
  NONE_64_MASK_TEST(MASK_LOGICAL_UNARY_TEST_SINGLE, name)

#define MASK_LOGICAL_BIN_TEST_SINGLE(name, ratio)                           \
  OP_TEST(name##_m_##ratio, name, rvv::vmask_t<ratio>, rvv::vmask_t<ratio>, \
          (rvv::vmask_t<ratio>, vs2), (rvv::vmask_t<ratio>, vs1),           \
          (rvv::vl_t<ratio>, vl))

#define MASK_LOGICAL_BIN_TEST(name) \
  NONE_64_MASK_TEST(MASK_LOGICAL_BIN_TEST_SINGLE, name)

MASK_LOGICAL_BIN_TEST(vmand);
MASK_LOGICAL_BIN_TEST(vmnand);
MASK_LOGICAL_BIN_TEST(vmandn);
MASK_LOGICAL_BIN_TEST(vmxor);
MASK_LOGICAL_BIN_TEST(vmor);
MASK_LOGICAL_BIN_TEST(vmnor);
MASK_LOGICAL_BIN_TEST(vmorn);
MASK_LOGICAL_BIN_TEST(vmxnor);
MASK_LOGICAL_UNARY_TEST(vmmv);
MASK_LOGICAL_NULLARY_TEST(vmclr);
MASK_LOGICAL_NULLARY_TEST(vmset);
MASK_LOGICAL_UNARY_TEST(vmnot);

#if HAS_ELEN64
MASK_LOGICAL_BIN_TEST_SINGLE(vmand, 64);
MASK_LOGICAL_BIN_TEST_SINGLE(vmnand, 64);
MASK_LOGICAL_BIN_TEST_SINGLE(vmandn, 64);
MASK_LOGICAL_BIN_TEST_SINGLE(vmxor, 64);
MASK_LOGICAL_BIN_TEST_SINGLE(vmor, 64);
MASK_LOGICAL_BIN_TEST_SINGLE(vmnor, 64);
MASK_LOGICAL_BIN_TEST_SINGLE(vmorn, 64);
MASK_LOGICAL_BIN_TEST_SINGLE(vmxnor, 64);
MASK_LOGICAL_UNARY_TEST_SINGLE(vmmv, 64);
MASK_LOGICAL_NULLARY_TEST_SINGLE(vmclr, 64);
MASK_LOGICAL_NULLARY_TEST_SINGLE(vmset, 64);
MASK_LOGICAL_UNARY_TEST_SINGLE(vmnot, 64);
#endif
