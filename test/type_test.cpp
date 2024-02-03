// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <gtest/gtest.h>
#include <rvv/config.h>
#include <rvv/type.h>

#include <cstddef>

template <typename Config>
class IsSupportedLMulTest : public ::testing::Test {};

template <rvv::LMul kLMul_, bool kExpected_>
class IsSupportedLMulConfig {
 public:
  static constexpr rvv::LMul kLMul = kLMul_;
  static constexpr bool kExpected = kExpected_;
};

using IsSupportedLMulTestTypes =
    ::testing::Types<IsSupportedLMulConfig<static_cast<rvv::LMul>(-4), false>,
                     IsSupportedLMulConfig<rvv::LMul::kM8, true>,
                     IsSupportedLMulConfig<rvv::LMul::kM4, true>,
                     IsSupportedLMulConfig<rvv::LMul::kM2, true>,
                     IsSupportedLMulConfig<rvv::LMul::kM1, true>,
                     IsSupportedLMulConfig<rvv::LMul::kMF2, true>,
                     IsSupportedLMulConfig<rvv::LMul::kMF4, true>,
                     IsSupportedLMulConfig<rvv::LMul::kMF8, true>,
                     IsSupportedLMulConfig<static_cast<rvv::LMul>(4), false>>;

TYPED_TEST_SUITE(IsSupportedLMulTest, IsSupportedLMulTestTypes);

TYPED_TEST(IsSupportedLMulTest, is_supported_lmul) {
  EXPECT_EQ((rvv::is_supported_lmul<TypeParam::kLMul>), TypeParam::kExpected);
}

template <typename Config>
class LMulRatioTest : public ::testing::Test {};

template <typename E, size_t kRatio_, rvv::LMul kLMul_>
class LMulRatioTestConfig {
 public:
  using ElemType = E;
  static constexpr size_t kRatio = kRatio_;
  static constexpr rvv::LMul kLMul = kLMul_;
};

using LMulRatioTestConfigs = ::testing::Types<
#if RVV_ELEN >= 64
    LMulRatioTestConfig<uint8_t, 64, rvv::LMul::kMF8>,
    LMulRatioTestConfig<uint16_t, 64, rvv::LMul::kMF4>,
#ifdef __riscv_zve64x
    LMulRatioTestConfig<uint64_t, 64, rvv::LMul::kM1>,
#endif
#endif
#ifdef __riscv_zve64x
    LMulRatioTestConfig<uint64_t, 8, rvv::LMul::kM8>,
#endif
    LMulRatioTestConfig<uint8_t, 1, rvv::LMul::kM8>,
    LMulRatioTestConfig<uint16_t, 2, rvv::LMul::kM8>>;

TYPED_TEST_SUITE(LMulRatioTest, LMulRatioTestConfigs);

TYPED_TEST(LMulRatioTest, lmul) {
  EXPECT_EQ((rvv::lmul<typename TypeParam::ElemType, TypeParam::kRatio>),
            TypeParam::kLMul);
}
TYPED_TEST(LMulRatioTest, ratio) {
  EXPECT_EQ((rvv::ratio<typename TypeParam::ElemType, TypeParam::kLMul>),
            TypeParam::kRatio);
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
    IsCompatibleElemRatioConfig<double, 8, RVV_ELEN >= 64 && HAS_ZVE64D>>;

TYPED_TEST_SUITE(IsCompatibleElemRatioTest, IsCompatibleElemRatioTestConfigs);

TYPED_TEST(IsCompatibleElemRatioTest, is_compatible_elem_ratio) {
  EXPECT_EQ((rvv::is_compatible_elem_ratio<typename TypeParam::ElemType,
                                           TypeParam::kRatio>),
            TypeParam::kExpected);
}

template <typename E, rvv::LMul kLMul_, bool kExpected_>
class IsCompatibleElemLMulConfig {
 public:
  using ElemType = E;
  static constexpr rvv::LMul kLMul = kLMul_;
  static constexpr bool kExpected = kExpected_;
};

template <typename Config>
class IsCompatibleElemLMulTest : public ::testing::Test {};

using IsCompatibleElemLMulTestTypes = ::testing::Types<
    IsCompatibleElemLMulConfig<uint8_t, rvv::LMul::kM8, true>,
    IsCompatibleElemLMulConfig<uint8_t, rvv::LMul::kM1, true>,
    IsCompatibleElemLMulConfig<uint8_t, rvv::LMul::kMF8, RVV_ELEN >= 64>,
    IsCompatibleElemLMulConfig<uint16_t, rvv::LMul::kM8, true>,
    IsCompatibleElemLMulConfig<uint16_t, rvv::LMul::kM1, true>,
    IsCompatibleElemLMulConfig<uint16_t, rvv::LMul::kMF4, RVV_ELEN >= 64>,
    IsCompatibleElemLMulConfig<uint16_t, rvv::LMul::kMF8, false>,
    IsCompatibleElemLMulConfig<uint64_t, rvv::LMul::kM8,
                               RVV_ELEN >= 64 && HAS_ZVE64X>,
    IsCompatibleElemLMulConfig<uint64_t, rvv::LMul::kM1,
                               RVV_ELEN >= 64 && HAS_ZVE64X>,
    IsCompatibleElemLMulConfig<uint64_t, rvv::LMul::kMF2, false>,
    IsCompatibleElemLMulConfig<uint64_t, rvv::LMul::kMF8, false>,
    IsCompatibleElemLMulConfig<void, rvv::LMul::kM8, false>,
    IsCompatibleElemLMulConfig<uint8_t, static_cast<rvv::LMul>(-4), false>,
#if HAS_FLOAT16
    IsCompatibleElemLMulConfig<_Float16, rvv::LMul::kM8, HAS_ZVFHMIN>,
#endif
    IsCompatibleElemLMulConfig<float, rvv::LMul::kM8, HAS_ZVE32F>,
    IsCompatibleElemLMulConfig<double, rvv::LMul::kM8,
                               RVV_ELEN >= 64 && HAS_ZVE64D>>;

TYPED_TEST_SUITE(IsCompatibleElemLMulTest, IsCompatibleElemLMulTestTypes);

TYPED_TEST(IsCompatibleElemLMulTest, is_compatible_elem_lmul) {
  EXPECT_EQ((rvv::is_compatible_elem_lmul<typename TypeParam::ElemType,
                                          TypeParam::kLMul>),
            TypeParam::kExpected);
}
