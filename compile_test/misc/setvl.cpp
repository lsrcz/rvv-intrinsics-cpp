// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/misc.h>

#define SETVL_TEST(ratio, short_name, lmul)                                 \
  rvv::vl_t<ratio> vsetvl##_vv_##short_name##_##ratio(size_t avl) {         \
    return rvv::vsetvl<ratio>(avl);                                         \
  }                                                                         \
  rvv::vl_t<ratio> vsetvl##_vv_##short_name##_##lmul(size_t avl) {          \
    return rvv::vsetvl<C_TYPE_NAME(short_name), CPP_LMUL_VALUE(lmul)>(avl); \
  }                                                                         \
  rvv::vl_t<ratio> vsetvl##_vv_##short_name##_##ratio() {                   \
    return rvv::vsetvlmax<ratio>();                                         \
  }                                                                         \
  rvv::vl_t<ratio> vsetvl##_vv_##short_name##_##lmul() {                    \
    return rvv::vsetvlmax<C_TYPE_NAME(short_name), CPP_LMUL_VALUE(lmul)>(); \
  }

SETVL_TEST(16, i16, m1);
#if HAS_ZVE32F
SETVL_TEST(32, f32, m1);
#endif
