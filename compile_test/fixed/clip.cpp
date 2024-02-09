// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fixed.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fixed.h>
#include <rvv/policy/tu/fixed.h>
#include <rvv/policy/tumu/fixed.h>

#define CLIP_VV_OP_TEST(name, func, ratio, short_name, lmul)                 \
  OP_TEST_ALL(                                                               \
      name##_vv_##short_name##lmul, func, rvv::vmask_t<ratio>,               \
      VREG_NAME(short_name, lmul), (WIDEN_VREG_NAME(short_name, lmul), vs2), \
      (UNSIGNED_VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));

#define CLIP_VX_OP_TEST(name, func, ratio, short_name, lmul)           \
  OP_TEST_ALL(name##_vx_##short_name##lmul, func, rvv::vmask_t<ratio>, \
              VREG_NAME(short_name, lmul),                             \
              (WIDEN_VREG_NAME(short_name, lmul), vs2), (size_t, rs1), \
              (rvv::vl_t<ratio>, vl));

#define CLIP_BIN_OP_TEST(name, func, ratio, short_name, lmul) \
  CLIP_VV_OP_TEST(name, func, ratio, short_name, lmul)        \
  CLIP_VX_OP_TEST(name, func, ratio, short_name, lmul)

CLIP_BIN_OP_TEST(vnclip, vnclip<rvv::VXRM::kRDN>, 8, i8, m1);
CLIP_BIN_OP_TEST(vnclipu, vnclipu<rvv::VXRM::kRDN>, 8, u8, m1);
