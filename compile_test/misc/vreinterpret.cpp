// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>

#define VREINTERPRET_VREG2VREG_TEST(short_name_from, lmul_from, short_name_to,   \
                                    lmul_to)                                     \
  VREG_NAME(short_name_to, lmul_to)                                              \
  vreinterpret##_v_v_##short_name_from##_##lmul_from##short_name_to##_##lmul_to( \
      VREG_NAME(short_name_from, lmul_from) a) {                                 \
    return rvv::vreinterpret<VREG_NAME(short_name_to, lmul_to)>(a);              \
  }                                                                              \
  static_assert(true, "Require trailing semicolon")

#define INT_SAME_SEW_SAME_LMUL_TEST(width, lmul)               \
  VREINTERPRET_VREG2VREG_TEST(i##width, lmul, u##width, lmul); \
  VREINTERPRET_VREG2VREG_TEST(u##width, lmul, i##width, lmul)

#define FP_SAME_SEW_SAME_LMUL_TEST(width, lmul)                \
  VREINTERPRET_VREG2VREG_TEST(f##width, lmul, u##width, lmul); \
  VREINTERPRET_VREG2VREG_TEST(u##width, lmul, f##width, lmul); \
  VREINTERPRET_VREG2VREG_TEST(f##width, lmul, i##width, lmul); \
  VREINTERPRET_VREG2VREG_TEST(i##width, lmul, f##width, lmul)

INT_SAME_SEW_SAME_LMUL_TEST(8, mf2);
INT_SAME_SEW_SAME_LMUL_TEST(16, m2);
INT_SAME_SEW_SAME_LMUL_TEST(32, m1);
#if HAS_ZVE64X
INT_SAME_SEW_SAME_LMUL_TEST(64, m2);
#endif

#if HAS_ZVFH
FP_SAME_SEW_SAME_LMUL_TEST(16, m2);
#endif

#if HAS_ZVE32F
FP_SAME_SEW_SAME_LMUL_TEST(32, m1);
#endif

#if HAS_ZVE64D
FP_SAME_SEW_SAME_LMUL_TEST(64, m2);
#endif

#define VREINTERPRET_MASK_TEST(ratio_from, short_name_to)                      \
  VREG_NAME(short_name_to, m1)                                                 \
  vreinterpret##_m_v_##ratio_from##short_name_to(rvv::vmask_t<ratio_from> a) { \
    return rvv::vreinterpret<VREG_NAME(short_name_to, m1)>(a);                 \
  }                                                                            \
  rvv::vmask_t<ratio_from> vreinterpret##_v_m_##ratio_from##short_name_to(     \
      VREG_NAME(short_name_to, m1) a) {                                        \
    return rvv::vreinterpret<rvv::vmask_t<ratio_from>>(a);                     \
  }                                                                            \
  static_assert(true, "Require trailing semicolon")

VREINTERPRET_MASK_TEST(1, i8);
VREINTERPRET_MASK_TEST(1, i32);
VREINTERPRET_MASK_TEST(32, i32);
VREINTERPRET_MASK_TEST(2, u8);
VREINTERPRET_MASK_TEST(4, u32);
VREINTERPRET_MASK_TEST(32, u32);
#if HAS_ZVE64X
VREINTERPRET_MASK_TEST(64, i32);
VREINTERPRET_MASK_TEST(1, i64);
VREINTERPRET_MASK_TEST(64, u8);
VREINTERPRET_MASK_TEST(4, u64);
#endif
