// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/load_store.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/load_store.h>
#include <rvv/policy/tu/load_store.h>
#include <rvv/policy/tumu/load_store.h>

#define VLM_TEST(ratio)                                              \
  OP_TEST(vlm##ratio, vlm, rvv::vmask_t<ratio>, rvv::vmask_t<ratio>, \
          (CONST_PTR(uint8_t), rs1), (rvv::vl_t<ratio>, vl))
#define VSM_TEST(ratio)                                                    \
  OP_TEST(vsm##ratio, vsm, rvv::vmask_t<ratio>, void, (PTR(uint8_t), rs1), \
          (rvv::vmask_t<ratio>, vs3), (rvv::vl_t<ratio>, vl))
#define MASK_TEST(ratio) \
  VLM_TEST(ratio);       \
  VSM_TEST(ratio)

MASK_TEST(1);
MASK_TEST(2);
MASK_TEST(4);
MASK_TEST(8);
MASK_TEST(16);
MASK_TEST(32);
MASK_TEST(64);
