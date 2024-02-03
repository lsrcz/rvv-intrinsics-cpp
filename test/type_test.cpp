// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <gtest/gtest.h>
#include <rvv/config.h>
#include <rvv/type.h>

#include <cstddef>

template <typename Config>
class LMulTest : public ::testing::Test {};

template <typename E, size_t kRatio_, rvv::LMul kExpected_>
class LMulTestConfig {
 public:
  using ElemType = E;
  static constexpr size_t kRatio = kRatio_;
  static constexpr rvv::LMul kExpected = kExpected_;
};

using LMulTestConfigs = ::testing::Types<
#if RVV_ELEN >= 64
    LMulTestConfig<uint8_t, 64, rvv::LMul::kMF8>,
    LMulTestConfig<uint16_t, 64, rvv::LMul::kMF4>,
#ifdef __riscv_zve64x
    LMulTestConfig<uint64_t, 64, rvv::LMul::kM1>,
#endif
#endif
#ifdef __riscv_zve64x
    LMulTestConfig<uint64_t, 8, rvv::LMul::kM8>,
#endif
    LMulTestConfig<uint8_t, 1, rvv::LMul::kM8>,
    LMulTestConfig<uint16_t, 2, rvv::LMul::kM8>>;

TYPED_TEST_SUITE(LMulTest, LMulTestConfigs);

TYPED_TEST(LMulTest, lmul) {
  EXPECT_EQ((rvv::lmul<typename TypeParam::ElemType, TypeParam::kRatio>),
            TypeParam::kExpected);
}

template <typename E, size_t kRatio_, bool kExpected_>
class IsCompatibleElemRatioConfig {
 public:
  using ElemType = E;
  static constexpr size_t kRatio = kRatio_;
  static constexpr bool kExpected = kExpected_;
};

template <typename Config>
class IsCompatibleElemRatioTest : public ::testing::Test {};

using IsCompatibleElemRatioTestConfigs = ::testing::Types<
    IsCompatibleElemRatioConfig<uint8_t, 64, RVV_ELEN >= 64>,
    IsCompatibleElemRatioConfig<uint16_t, 64, RVV_ELEN >= 64>,
    IsCompatibleElemRatioConfig<uint32_t, 64, RVV_ELEN >= 64>,
    IsCompatibleElemRatioConfig<uint64_t, 64, RVV_ELEN >= 64 && HAS_ZVE64X>,
    IsCompatibleElemRatioConfig<uint8_t, 8, true>,
    IsCompatibleElemRatioConfig<uint16_t, 8, true>,
    IsCompatibleElemRatioConfig<uint32_t, 8, true>,
    IsCompatibleElemRatioConfig<uint64_t, 8, RVV_ELEN >= 64 && HAS_ZVE64X>,
    IsCompatibleElemRatioConfig<uint8_t, 4, true>,
    IsCompatibleElemRatioConfig<uint16_t, 4, true>,
    IsCompatibleElemRatioConfig<uint32_t, 4, true>,
    IsCompatibleElemRatioConfig<uint64_t, 4, false>,
    IsCompatibleElemRatioConfig<uint8_t, 1, true>,
    IsCompatibleElemRatioConfig<uint16_t, 1, false>,
    IsCompatibleElemRatioConfig<uint32_t, 1, false>,
    IsCompatibleElemRatioConfig<uint64_t, 1, false>,
    IsCompatibleElemRatioConfig<uint8_t, 3, false>,
    IsCompatibleElemRatioConfig<void, 1, false>,
#if HAS_FLOAT16
    IsCompatibleElemRatioConfig<_Float16, 8, HAS_ZVFHMIN>,
#endif
    IsCompatibleElemRatioConfig<float, 8, HAS_ZVE32F>,
    IsCompatibleElemRatioConfig<double, 8, HAS_ZVE64D>>;

TYPED_TEST_SUITE(IsCompatibleElemRatioTest, IsCompatibleElemRatioTestConfigs);

TYPED_TEST(IsCompatibleElemRatioTest, is_compatible_elem_ratio) {
  EXPECT_EQ((rvv::is_compatible_elem_ratio<typename TypeParam::ElemType,
                                           TypeParam::kRatio>),
            TypeParam::kExpected);
}
