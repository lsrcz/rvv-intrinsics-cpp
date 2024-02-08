// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

#define ADC_SBC_VXM_TEST(name, ratio, short_name, lmul)                      \
  OP_TEST_NO_MASK(name##_vxm_##short_name##lmul, name, rvv::vmask_t<ratio>,  \
                  VREG_NAME(short_name, lmul),                               \
                  (VREG_NAME(short_name, lmul), vs2),                        \
                  (C_TYPE_NAME(short_name), rs1), (rvv::vmask_t<ratio>, v0), \
                  (rvv::vl_t<ratio>, vl));
#define ADC_SBC_VVM_TEST(name, ratio, short_name, lmul)                     \
  OP_TEST_NO_MASK(name##_vxm_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  VREG_NAME(short_name, lmul),                              \
                  (VREG_NAME(short_name, lmul), vs2),                       \
                  (VREG_NAME(short_name, lmul), vs1),                       \
                  (rvv::vmask_t<ratio>, v0), (rvv::vl_t<ratio>, vl));

ADC_SBC_VXM_TEST(vadc, 2, i16, m8)
ADC_SBC_VXM_TEST(vsbc, 8, u16, m2)
ADC_SBC_VVM_TEST(vadc, 2, i16, m8)
ADC_SBC_VVM_TEST(vsbc, 8, u16, m2)

#define CARRY_OUT_VX_TEST(name, ratio, short_name, lmul)           \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
          rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2), \
          (C_TYPE_NAME(short_name), vs1), (rvv::vl_t<ratio>, vl));
#define CARRY_OUT_VV_TEST(name, ratio, short_name, lmul)           \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
          rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2), \
          (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define CARRY_OUT_VXM_TEST(name, ratio, short_name, lmul)            \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,   \
          rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2),   \
          (C_TYPE_NAME(short_name), vs1), (rvv::vmask_t<ratio>, v0), \
          (rvv::vl_t<ratio>, vl));
#define CARRY_OUT_VVM_TEST(name, ratio, short_name, lmul)                \
  OP_TEST(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,       \
          rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2),       \
          (VREG_NAME(short_name, lmul), vs1), (rvv::vmask_t<ratio>, v0), \
          (rvv::vl_t<ratio>, vl));
#define CARRY_OUT_TEST(name, ratio, short_name, lmul) \
  CARRY_OUT_VX_TEST(name, ratio, short_name, lmul)    \
  CARRY_OUT_VV_TEST(name, ratio, short_name, lmul)    \
  CARRY_OUT_VXM_TEST(name, ratio, short_name, lmul)   \
  CARRY_OUT_VVM_TEST(name, ratio, short_name, lmul)

CARRY_OUT_TEST(vmadc, 2, i16, m8)
CARRY_OUT_TEST(vmsbc, 2, i16, m8)
