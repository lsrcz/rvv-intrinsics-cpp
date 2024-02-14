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
  EXPECT_EQ((rvv::SupportedLMul<TypeParam::kLMul>), TypeParam::kExpected);
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
  EXPECT_EQ((rvv::CompatibleElemRatio<typename TypeParam::ElemType,
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
  EXPECT_EQ(
      (rvv::CompatibleElemLMul<typename TypeParam::ElemType, TypeParam::kLMul>),
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
class VTupleTypeTest : public ::testing::Test {};

template <typename E, size_t kRatio_, size_t kTupleSize_, typename R>
class VTupleTypeConfig {
 public:
  using ElemType = E;
  static constexpr size_t kRatio = kRatio_;
  static constexpr size_t kTupleSize = kTupleSize_;
  using RegType = R;
};

using VTupleTypeTestConfigs = ::testing::Types<
#if HAS_ELEN64
    VTupleTypeConfig<uint8_t, 64, 2, vuint8mf8x2_t>,
    VTupleTypeConfig<uint8_t, 64, 8, vuint8mf8x8_t>,
    VTupleTypeConfig<int16_t, 64, 2, vint16mf4x2_t>,
    VTupleTypeConfig<int16_t, 64, 8, vint16mf4x8_t>,
    VTupleTypeConfig<int32_t, 64, 2, vint32mf2x2_t>,
    VTupleTypeConfig<int32_t, 64, 8, vint32mf2x8_t>,
#if HAS_ZVE64X
    VTupleTypeConfig<uint64_t, 64, 2, vuint64m1x2_t>,
    VTupleTypeConfig<uint64_t, 64, 8, vuint64m1x8_t>,
#endif
#endif
#if HAS_ZVFHMIN
    VTupleTypeConfig<_Float16, 4, 2, vfloat16m4x2_t>,
#endif
#if HAS_ZVE32F
    VTupleTypeConfig<float, 16, 2, vfloat32m2x2_t>,
    VTupleTypeConfig<float, 16, 4, vfloat32m2x4_t>,
#endif
#if HAS_ZVE64D
    VTupleTypeConfig<double, 32, 2, vfloat64m2x2_t>,
    VTupleTypeConfig<double, 32, 4, vfloat64m2x4_t>,
#endif
    VTupleTypeConfig<uint8_t, 2, 2, vuint8m4x2_t>,
    VTupleTypeConfig<uint8_t, 4, 2, vuint8m2x2_t>,
    VTupleTypeConfig<uint8_t, 4, 4, vuint8m2x4_t>,
    VTupleTypeConfig<uint8_t, 8, 2, vuint8m1x2_t>,
    VTupleTypeConfig<uint8_t, 8, 8, vuint8m1x8_t>>;

TYPED_TEST_SUITE(VTupleTypeTest, VTupleTypeTestConfigs);

TYPED_TEST(VTupleTypeTest, vreg) {
  using Actual = rvv::vtuple_t<typename TypeParam::ElemType, TypeParam::kRatio,
                               TypeParam::kTupleSize>;
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
    ElemTypeConfig<vint32m8_t, int32_t>, ElemTypeConfig<vint32m1_t, int32_t>,
    ElemTypeConfig<vuint8m1x2_t, uint8_t>>;

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
    RatioConfig<rvv::vl_t<8>, 8>, RatioConfig<rvv::vmask_t<8>, 8>,
    RatioConfig<vint32m1x2_t, 32>>;

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

enum SupportedVReg {
  kIsVReg = 1,
  kIsSupportedIntegralVReg = 2,
  kIsSupportedFloatingPointVReg = 4,
  kIsSupportedFloatingPointVRegWithZvfh = 8,
  kIsSupportedSignedVReg = 16,
  kIsSupportedUnsignedVReg = 32,
};

template <typename Config>
class IsVRegTest : public ::testing::Test {};

template <typename T_, SupportedVReg kSpec_>
class IsVRegConfig {
 public:
  using T = T_;
  static constexpr SupportedVReg kSpec = kSpec_;
};

using IsVRegConfigs = ::testing::Types<
#if HAS_ELEN64
    IsVRegConfig<vuint8mf8_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedUnsignedVReg)>,
    IsVRegConfig<vint16mf4_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedSignedVReg)>,
    IsVRegConfig<vint32mf2_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedSignedVReg)>,
#if HAS_ZVE64X
    IsVRegConfig<vuint64m8_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedUnsignedVReg)>,
    IsVRegConfig<vuint64m1_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedUnsignedVReg)>,
#endif
#endif
#if HAS_ZVFH
    IsVRegConfig<vfloat16m8_t, static_cast<SupportedVReg>(
                                   kIsVReg | kIsSupportedFloatingPointVReg |
                                   kIsSupportedFloatingPointVRegWithZvfh)>,
#elif HAS_ZVFHMIN
    IsVRegConfig<vfloat16m8_t, static_cast<SupportedVReg>(
                                   kIsVReg | kIsSupportedFloatingPointVReg)>,
#endif

#if HAS_ZVE32F
    IsVRegConfig<vfloat32m8_t, static_cast<SupportedVReg>(
                                   kIsVReg | kIsSupportedFloatingPointVReg |
                                   kIsSupportedFloatingPointVRegWithZvfh)>,
#endif
#if HAS_ZVE64D
    IsVRegConfig<vfloat64m8_t, static_cast<SupportedVReg>(
                                   kIsVReg | kIsSupportedFloatingPointVReg |
                                   kIsSupportedFloatingPointVRegWithZvfh)>,
#endif
    IsVRegConfig<vuint8m8_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedUnsignedVReg)>,
    IsVRegConfig<vuint8mf4_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedUnsignedVReg)>,
    IsVRegConfig<vint16m8_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedSignedVReg)>,
    IsVRegConfig<vint16mf2_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedSignedVReg)>,
    IsVRegConfig<vint32m8_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedSignedVReg)>,
    IsVRegConfig<vint32m1_t,
                 static_cast<SupportedVReg>(kIsVReg | kIsSupportedIntegralVReg |
                                            kIsSupportedSignedVReg)>,
    IsVRegConfig<rvv::vl_t<8>, static_cast<SupportedVReg>(0)>,
    IsVRegConfig<rvv::vmask_t<8>, static_cast<SupportedVReg>(0)>,
    IsVRegConfig<int8_t, static_cast<SupportedVReg>(0)>>;

TYPED_TEST_SUITE(IsVRegTest, IsVRegConfigs);

TYPED_TEST(IsVRegTest, is_vreg) {
  EXPECT_EQ((rvv::IsVReg<typename TypeParam::T>),
            !!(TypeParam::kSpec & SupportedVReg::kIsVReg));
}

TYPED_TEST(IsVRegTest, is_supported_integral_vreg) {
  EXPECT_EQ((rvv::SupportedIntegralVReg<typename TypeParam::T>),
            !!(TypeParam::kSpec & SupportedVReg::kIsSupportedIntegralVReg));
}

TYPED_TEST(IsVRegTest, is_supported_floating_point_vreg) {
  EXPECT_EQ(
      (rvv::SupportedFloatingPointVReg<typename TypeParam::T, false>),
      !!(TypeParam::kSpec & SupportedVReg::kIsSupportedFloatingPointVReg));
}

TYPED_TEST(IsVRegTest, is_supported_floating_point_vreg_with_zvfh) {
  EXPECT_EQ((rvv::SupportedFloatingPointVReg<typename TypeParam::T, true>),
            !!(TypeParam::kSpec &
               SupportedVReg::kIsSupportedFloatingPointVRegWithZvfh));
}

TYPED_TEST(IsVRegTest, is_supported_signed_vreg) {
  EXPECT_EQ((rvv::SupportedSignedVReg<typename TypeParam::T>),
            !!(TypeParam::kSpec & SupportedVReg::kIsSupportedSignedVReg));
}

TYPED_TEST(IsVRegTest, is_supported_unsigned_vreg) {
  EXPECT_EQ((rvv::SupportedUnsignedVReg<typename TypeParam::T>),
            !!(TypeParam::kSpec & SupportedVReg::kIsSupportedUnsignedVReg));
}

template <typename Config>
class IsCompatibleVRegRatioTest : public ::testing::Test {};

template <typename T_, size_t kRatio_, bool kExpected_>
class IsCompatibleVRegRatioConfig {
 public:
  using T = T_;
  static constexpr size_t kRatio = kRatio_;
  static constexpr bool kExpected = kExpected_;
};

using IsCompatibleVRegRatioConfigs = ::testing::Types<
#if HAS_ELEN64
    IsCompatibleVRegRatioConfig<vuint8mf8_t, 64, true>,
    IsCompatibleVRegRatioConfig<vint16mf4_t, 64, true>,
    IsCompatibleVRegRatioConfig<vint32mf2_t, 64, true>,
#if HAS_ZVE64X
    IsCompatibleVRegRatioConfig<vuint64m8_t, 8, true>,
    IsCompatibleVRegRatioConfig<vuint64m1_t, 64, true>,
#endif
#endif
#if HAS_ZVFHMIN
    IsCompatibleVRegRatioConfig<vfloat16m8_t, 2, true>,
#endif
#if HAS_ZVE32F
    IsCompatibleVRegRatioConfig<vfloat32m8_t, 4, true>,
#endif
#if HAS_ZVE64D
    IsCompatibleVRegRatioConfig<vfloat64m8_t, 8, true>,
#endif
    IsCompatibleVRegRatioConfig<vuint8m8_t, 1, true>,
    IsCompatibleVRegRatioConfig<vuint8mf4_t, 32, true>,
    IsCompatibleVRegRatioConfig<vint16m8_t, 2, true>,
    IsCompatibleVRegRatioConfig<vint16mf2_t, 32, true>,
    IsCompatibleVRegRatioConfig<vint32m8_t, 4, true>,
    IsCompatibleVRegRatioConfig<vint32m1_t, 32, true>,
    IsCompatibleVRegRatioConfig<vint32m1_t, 8, false>,
    IsCompatibleVRegRatioConfig<rvv::vl_t<8>, 8, false>,
    IsCompatibleVRegRatioConfig<rvv::vmask_t<8>, 8, false>,
    IsCompatibleVRegRatioConfig<int8_t, 8, false>>;

TYPED_TEST_SUITE(IsCompatibleVRegRatioTest, IsCompatibleVRegRatioConfigs);

TYPED_TEST(IsCompatibleVRegRatioTest, is_compatible_vreg_ratio) {
  EXPECT_EQ(
      (rvv::CompatibleVRegRatio<typename TypeParam::T, TypeParam::kRatio>),
      TypeParam::kExpected);
}

template <typename Config>
class VRegM1TypeTest : public ::testing::Test {};

template <typename V_, typename VRegM1_>
class VRegM1TypeConfig {
 public:
  using V = V_;
  using VRegM1 = VRegM1_;
};

using VRegM1TypeTestConfigs =
    ::testing::Types<VRegM1TypeConfig<vuint8mf4_t, vuint8m1_t>,
                     VRegM1TypeConfig<vint16m2_t, vint16m1_t>,
#if HAS_ZVE32F
                     VRegM1TypeConfig<vfloat32m2_t, vfloat32m1_t>,
#endif
                     VRegM1TypeConfig<vint32mf2_t, vint32m1_t>>;

TYPED_TEST_SUITE(VRegM1TypeTest, VRegM1TypeTestConfigs);

TYPED_TEST(VRegM1TypeTest, vreg_m1) {
  using Actual = rvv::vreg_m1_t<typename TypeParam::V>;
  EXPECT_TRUE((std::is_same_v<Actual, typename TypeParam::VRegM1>));
}

template <typename Config>
class ValidIndexTest : public ::testing::Test {};

template <typename VLarge_, typename VSmall_, size_t kIndex_, bool kExpected_>
class ValidIndexConfig {
 public:
  using VLarge = VLarge_;
  using VSmall = VSmall_;
  static constexpr size_t kIndex = kIndex_;
  static constexpr bool kExpected = kExpected_;
};

using ValidIndexConfigs =
    ::testing::Types<ValidIndexConfig<vuint8m8_t, vuint8m1_t, 0, true>,
                     ValidIndexConfig<vuint8m8_t, vuint8m1_t, 1, true>,
                     ValidIndexConfig<vuint8m8_t, vuint8m1_t, 7, true>,
                     ValidIndexConfig<vuint8m8_t, vuint8m1_t, 8, false>,
                     ValidIndexConfig<vuint8m8_t, vuint8m4_t, 0, true>,
                     ValidIndexConfig<vuint8m8_t, vuint8m4_t, 1, true>,
                     ValidIndexConfig<vuint8m8_t, vuint8m8_t, 0, false>,
                     ValidIndexConfig<vuint8m1_t, vuint8m1_t, 0, false>,
                     ValidIndexConfig<vuint8m1_t, vuint8mf2_t, 0, false>,
                     ValidIndexConfig<vuint8mf2_t, vuint8mf4_t, 0, false>,
                     ValidIndexConfig<vuint32m2_t, vuint8m1_t, 0, false>,
                     ValidIndexConfig<vuint32m2_t, vuint8m2_t, 0, false>,
                     ValidIndexConfig<vuint32m2_t, vuint32m1_t, 0, true>,
#if HAS_ZVE64X
                     ValidIndexConfig<vuint64m1_t, vuint64m1_t, 0, false>,
                     ValidIndexConfig<vuint64m2_t, vuint64m1_t, 0, true>,
                     ValidIndexConfig<vuint64m2_t, vuint64m1_t, 1, true>,
                     ValidIndexConfig<vuint64m2_t, vuint64m1_t, 2, false>,
#endif
#if HAS_ZVFH
                     ValidIndexConfig<vfloat64m4_t, vfloat64m1_t, 0, true>,
                     ValidIndexConfig<vfloat64m4_t, vfloat64m1_t, 3, true>,
                     ValidIndexConfig<vfloat64m4_t, vfloat64m1_t, 4, false>,
#endif
#if HAS_ZVE32F
                     ValidIndexConfig<vfloat32m4_t, vfloat32m1_t, 0, true>,
                     ValidIndexConfig<vfloat32m4_t, vfloat32m1_t, 3, true>,
                     ValidIndexConfig<vfloat32m4_t, vfloat32m1_t, 4, false>,
#endif
#if HAS_ZVE64D
                     ValidIndexConfig<vfloat64m4_t, vfloat64m1_t, 0, true>,
                     ValidIndexConfig<vfloat64m4_t, vfloat64m1_t, 3, true>,
                     ValidIndexConfig<vfloat64m4_t, vfloat64m1_t, 4, false>,
#endif
                     ValidIndexConfig<void, vuint32m1_t, 0, false>,
                     ValidIndexConfig<vuint32m2_t, void, 0, false>,
                     ValidIndexConfig<vint32m1x2_t, vint32m1_t, 0, true>,
                     ValidIndexConfig<vint32m1x2_t, vint32m1_t, 1, true>,
                     ValidIndexConfig<vint32m1x2_t, vint32m1_t, 2, false>,
                     ValidIndexConfig<vint32m1x6_t, vint32m1_t, 0, true>,
                     ValidIndexConfig<vint32m1x6_t, vint32m1_t, 5, true>,
                     ValidIndexConfig<vint32m1x6_t, vint32m1_t, 6, false>>;

TYPED_TEST_SUITE(ValidIndexTest, ValidIndexConfigs);

TYPED_TEST(ValidIndexTest, valid_index) {
  EXPECT_EQ((rvv::ValidIndex<typename TypeParam::VLarge,
                             typename TypeParam::VSmall, TypeParam::kIndex>),
            TypeParam::kExpected);
}