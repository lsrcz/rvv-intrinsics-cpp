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
  EXPECT_EQ((rvv::elem_ratio_to_lmul<typename TypeParam::ElemType,
                                     TypeParam::kRatio>),
            TypeParam::kLMul);
}
TYPED_TEST(LMulRatioTest, ratio) {
  EXPECT_EQ(
      (rvv::elem_lmul_to_ratio<typename TypeParam::ElemType, TypeParam::kLMul>),
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

template <typename Config>
class VRegTypeTest : public ::testing::Test {};

template <typename E, size_t kRatio_, typename R>
class VRegTypeConfig {
 public:
  using ElemType = E;
  static constexpr size_t kRatio = kRatio_;
  using RegType = R;
};

using VRegTypeTestConfigs = ::testing::Types<
#if HAS_ELEN64
    VRegTypeConfig<uint8_t, 64, vuint8mf8_t>,
    VRegTypeConfig<int16_t, 64, vint16mf4_t>,
    VRegTypeConfig<int32_t, 64, vint32mf2_t>,
#if HAS_ZVE64X
    VRegTypeConfig<uint64_t, 8, vuint64m8_t>,
    VRegTypeConfig<uint64_t, 64, vuint64m1_t>,
#endif
#endif
#if HAS_ZVFHMIN
    VRegTypeConfig<_Float16, 2, vfloat16m8_t>,
#endif
#if HAS_ZVE32F
    VRegTypeConfig<float, 4, vfloat32m8_t>,
#endif
#if HAS_ZVE64D
    VRegTypeConfig<double, 8, vfloat64m8_t>,
#endif
    VRegTypeConfig<uint8_t, 1, vuint8m8_t>,
    VRegTypeConfig<uint8_t, 32, vuint8mf4_t>,
    VRegTypeConfig<int16_t, 2, vint16m8_t>,
    VRegTypeConfig<int16_t, 32, vint16mf2_t>,
    VRegTypeConfig<int32_t, 4, vint32m8_t>,
    VRegTypeConfig<int32_t, 32, vint32m1_t>>;

TYPED_TEST_SUITE(VRegTypeTest, VRegTypeTestConfigs);

TYPED_TEST(VRegTypeTest, vreg) {
  using Actual = rvv::vreg_t<typename TypeParam::ElemType, TypeParam::kRatio>;
  EXPECT_TRUE((std::is_same_v<Actual, typename TypeParam::RegType>));
}

template <typename Config>
class ElemTypeTest : public ::testing::Test {};

template <typename T, typename E>
class ElemTypeConfig {
 public:
  using Type = T;
  using ElemType = E;
};

using ElemTTestConfigs = ::testing::Types<
#if HAS_ELEN64
    ElemTypeConfig<vuint8mf8_t, uint8_t>, ElemTypeConfig<vint16mf4_t, int16_t>,
    ElemTypeConfig<vint32mf2_t, int32_t>,
#if HAS_ZVE64X
    ElemTypeConfig<vuint64m8_t, uint64_t>,
    ElemTypeConfig<vuint64m1_t, uint64_t>,
#endif
#endif
#if HAS_ZVFHMIN
    ElemTypeConfig<vfloat16m8_t, _Float16>,
#endif
#if HAS_ZVE32F
    ElemTypeConfig<vfloat32m8_t, float>,
#endif
#if HAS_ZVE64D
    ElemTypeConfig<vfloat64m8_t, double>,
#endif
    ElemTypeConfig<vuint8m8_t, uint8_t>, ElemTypeConfig<vuint8mf4_t, uint8_t>,
    ElemTypeConfig<vint16m8_t, int16_t>, ElemTypeConfig<vint16mf2_t, int16_t>,
    ElemTypeConfig<vint32m8_t, int32_t>, ElemTypeConfig<vint32m1_t, int32_t>>;

TYPED_TEST_SUITE(ElemTypeTest, ElemTTestConfigs);

TYPED_TEST(ElemTypeTest, elem_type) {
  using Actual = rvv::elem_t<typename TypeParam::Type>;
  EXPECT_TRUE((std::is_same_v<Actual, typename TypeParam::ElemType>));
}

template <typename Config>
class RatioTest : public ::testing::Test {};

template <typename T, size_t kRatio_>
class RatioConfig {
 public:
  using Type = T;
  static constexpr size_t kRatio = kRatio_;
};

using RatioTestConfigs = ::testing::Types<
#if HAS_ELEN64
    RatioConfig<vuint8mf8_t, 64>, RatioConfig<vint16mf4_t, 64>,
    RatioConfig<vint32mf2_t, 64>,
#if HAS_ZVE64X
    RatioConfig<vuint64m8_t, 8>, RatioConfig<vuint64m1_t, 64>,
#endif
#endif
#if HAS_ZVFHMIN
    RatioConfig<vfloat16m8_t, 2>,
#endif
#if HAS_ZVE32F
    RatioConfig<vfloat32m8_t, 4>,
#endif
#if HAS_ZVE64D
    RatioConfig<vfloat64m8_t, 8>,
#endif
    RatioConfig<vuint8m8_t, 1>, RatioConfig<vuint8mf4_t, 32>,
    RatioConfig<vint16m8_t, 2>, RatioConfig<vint16mf2_t, 32>,
    RatioConfig<vint32m8_t, 4>, RatioConfig<vint32m1_t, 32>,
    RatioConfig<rvv::vl_t<8>, 8>, RatioConfig<rvv::vmask_t<8>, 8>>;

TYPED_TEST_SUITE(RatioTest, RatioTestConfigs);

TYPED_TEST(RatioTest, ratio) {
  EXPECT_EQ((rvv::ratio<typename TypeParam::Type>), TypeParam::kRatio);
}

template <typename Config>
class VMaskTypeTest : public ::testing::Test {};

template <size_t kRatio_, typename M>
class VMaskTypeConfig {
 public:
  static constexpr size_t kRatio = kRatio_;
  using MaskType = M;
};

using VMaskTypeTestConfigs = ::testing::Types<
#if HAS_ELEN64
    VMaskTypeConfig<64, vbool64_t>,
#endif
    VMaskTypeConfig<32, vbool32_t>, VMaskTypeConfig<16, vbool16_t>,
    VMaskTypeConfig<8, vbool8_t>, VMaskTypeConfig<4, vbool4_t>,
    VMaskTypeConfig<2, vbool2_t>, VMaskTypeConfig<1, vbool1_t>>;

TYPED_TEST_SUITE(VMaskTypeTest, VMaskTypeTestConfigs);

TYPED_TEST(VMaskTypeTest, vmask) {
  using Actual = rvv::vmask_t<TypeParam::kRatio>;
  EXPECT_TRUE((std::is_same_v<Actual, typename TypeParam::MaskType>));
}

template <typename Config>
class LMulTest : public ::testing::Test {};

template <typename T, rvv::LMul kLMul_>
class LMulConfig {
 public:
  using Type = T;
  static constexpr rvv::LMul kLMul = kLMul_;
};

using LMulTestConfigs = ::testing::Types<
#if HAS_ELEN64
    LMulConfig<vuint8mf8_t, rvv::LMul::kMF8>,
    LMulConfig<vint16mf4_t, rvv::LMul::kMF4>,
    LMulConfig<vint32mf2_t, rvv::LMul::kMF2>,
#if HAS_ZVE64X
    LMulConfig<vuint64m8_t, rvv::LMul::kM8>,
    LMulConfig<vuint64m1_t, rvv::LMul::kM1>,
#endif
#endif
#if HAS_ZVFHMIN
    LMulConfig<vfloat16m8_t, rvv::LMul::kM8>,
#endif
#if HAS_ZVE32F
    LMulConfig<vfloat32m8_t, rvv::LMul::kM8>,
#endif
#if HAS_ZVE64D
    LMulConfig<vfloat64m8_t, rvv::LMul::kM8>,
#endif
    LMulConfig<vuint8m8_t, rvv::LMul::kM8>,
    LMulConfig<vuint8mf4_t, rvv::LMul::kMF4>,
    LMulConfig<vint16m8_t, rvv::LMul::kM8>,
    LMulConfig<vint16mf2_t, rvv::LMul::kMF2>,
    LMulConfig<vint32m8_t, rvv::LMul::kM8>,
    LMulConfig<vint32m1_t, rvv::LMul::kM1>>;

TYPED_TEST_SUITE(LMulTest, LMulTestConfigs);

TYPED_TEST(LMulTest, lmul) {
  EXPECT_EQ((rvv::lmul<typename TypeParam::Type>), TypeParam::kLMul);
}
