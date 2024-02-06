// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <gtest/gtest.h>
#include <rvv/type.h>

template <typename Config>
class IsAnyTest : public ::testing::Test {};

template <bool kExpected_, typename E, typename... Es>
class IsAnyConfig {
 public:
  static constexpr bool kActual = rvv::is_any<E, Es...>;
  static constexpr bool kExpected = kExpected_;
};

using IsAnyTestTypes =
    ::testing::Types<IsAnyConfig<true, int, int, float, double>,
                     IsAnyConfig<true, float, int, float, double>,
                     IsAnyConfig<true, double, int, float, double>,
                     IsAnyConfig<false, char, int, float, double>>;

TYPED_TEST_SUITE(IsAnyTest, IsAnyTestTypes);

TYPED_TEST(IsAnyTest, is_any) {
  EXPECT_EQ(TypeParam::kActual, TypeParam::kExpected);
}

enum ElemTypeTraits {
  kIsFloat16 = 1,
  kIsFloat32 = 2,
  kIsFloat64 = 4,
  kIsRvvFloatingPoint = 8,
  kIsRvvUnsigned = 16,
  kIsRvvSigned = 32,
  kIsRvvIntegral = 64,
  kReliesUnsupportedZvfhmin = 128,
  kReliesUnsupportedZvfh = 256,
  kReliesUnsupportedZve32f = 512,
  kReliesUnsupportedZve64d = 1024,
  kReliesUnsupportedZve64x = 2048,
  kIsSupportedRvvElemType = 4096,
  kIsSupportedRvvElemTypeNeedZvfh = 8192,
  kIsSupportedRvvIntegral = 16384,
  kIsSupportedRvvFloatingPoint = 32768,
  kIsSupportedRvvFloatingPointNeedZvfh = 65536,
};

template <typename Config>
class ElemTypeTraitsTest : public ::testing::Test {};

template <typename E, ElemTypeTraits kTrait_>
class ElemTypeTraitsConfig {
 public:
  using ElemType = E;
  static constexpr ElemTypeTraits kTrait = kTrait_;
};

using ElemTypeTraitsTestConfigs = ::testing::Types<
#if HAS_FLOAT16
    ElemTypeTraitsConfig<
        rvv::float16_t, static_cast<ElemTypeTraits>(
                            kIsFloat16 | kIsRvvFloatingPoint |
                            (HAS_ZVFH ? kIsSupportedRvvElemTypeNeedZvfh |
                                            kIsSupportedRvvFloatingPointNeedZvfh
                                      : kReliesUnsupportedZvfh) |
                            (HAS_ZVFHMIN ? kIsSupportedRvvElemType |
                                               kIsSupportedRvvFloatingPoint
                                         : kReliesUnsupportedZvfhmin))>,
#endif
    ElemTypeTraitsConfig<
        float, static_cast<ElemTypeTraits>(
                   kIsFloat32 | kIsRvvFloatingPoint |
                   (HAS_ZVE32F ? kIsSupportedRvvElemType |
                                     kIsSupportedRvvElemTypeNeedZvfh |
                                     kIsSupportedRvvFloatingPoint |
                                     kIsSupportedRvvFloatingPointNeedZvfh
                               : kReliesUnsupportedZve32f))>,
    ElemTypeTraitsConfig<
        double, static_cast<ElemTypeTraits>(
                    kIsFloat64 | kIsRvvFloatingPoint |
                    (HAS_ZVE64D ? kIsSupportedRvvElemType |
                                      kIsSupportedRvvElemTypeNeedZvfh |
                                      kIsSupportedRvvFloatingPoint |
                                      kIsSupportedRvvFloatingPointNeedZvfh
                                : kReliesUnsupportedZve64d))>,
    ElemTypeTraitsConfig<uint8_t, static_cast<ElemTypeTraits>(
                                      kIsRvvUnsigned | kIsRvvIntegral |
                                      kIsSupportedRvvElemType |
                                      kIsSupportedRvvElemTypeNeedZvfh |
                                      kIsSupportedRvvIntegral)>,
    ElemTypeTraitsConfig<uint16_t, static_cast<ElemTypeTraits>(
                                       kIsRvvUnsigned | kIsRvvIntegral |
                                       kIsSupportedRvvElemType |
                                       kIsSupportedRvvElemTypeNeedZvfh |
                                       kIsSupportedRvvIntegral)>,
    ElemTypeTraitsConfig<uint32_t, static_cast<ElemTypeTraits>(
                                       kIsRvvUnsigned | kIsRvvIntegral |
                                       kIsSupportedRvvElemType |
                                       kIsSupportedRvvElemTypeNeedZvfh |
                                       kIsSupportedRvvIntegral)>,
    ElemTypeTraitsConfig<uint64_t,
                         static_cast<ElemTypeTraits>(
                             kIsRvvUnsigned | kIsRvvIntegral |
                             (HAS_ZVE64X ? kIsSupportedRvvElemType |
                                               kIsSupportedRvvElemTypeNeedZvfh |
                                               kIsSupportedRvvIntegral
                                         : kReliesUnsupportedZve64x))>,
    ElemTypeTraitsConfig<
        int8_t, static_cast<ElemTypeTraits>(
                    kIsRvvSigned | kIsRvvIntegral | kIsSupportedRvvElemType |
                    kIsSupportedRvvElemTypeNeedZvfh | kIsSupportedRvvIntegral)>,
    ElemTypeTraitsConfig<int16_t, static_cast<ElemTypeTraits>(
                                      kIsRvvSigned | kIsRvvIntegral |
                                      kIsSupportedRvvElemType |
                                      kIsSupportedRvvElemTypeNeedZvfh |
                                      kIsSupportedRvvIntegral)>,
    ElemTypeTraitsConfig<int32_t, static_cast<ElemTypeTraits>(
                                      kIsRvvSigned | kIsRvvIntegral |
                                      kIsSupportedRvvElemType |
                                      kIsSupportedRvvElemTypeNeedZvfh |
                                      kIsSupportedRvvIntegral)>,
    ElemTypeTraitsConfig<int64_t,
                         static_cast<ElemTypeTraits>(
                             kIsRvvSigned | kIsRvvIntegral |
                             (HAS_ZVE64X ? kIsSupportedRvvElemType |
                                               kIsSupportedRvvElemTypeNeedZvfh |
                                               kIsSupportedRvvIntegral
                                         : kReliesUnsupportedZve64x))>

    >;

TYPED_TEST_SUITE(ElemTypeTraitsTest, ElemTypeTraitsTestConfigs);

TYPED_TEST(ElemTypeTraitsTest, is_float16) {
  EXPECT_EQ((rvv::is_float16<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kIsFloat16));
}

TYPED_TEST(ElemTypeTraitsTest, is_float32) {
  EXPECT_EQ((rvv::is_float32<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kIsFloat32));
}

TYPED_TEST(ElemTypeTraitsTest, is_float64) {
  EXPECT_EQ((rvv::is_float64<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kIsFloat64));
}

TYPED_TEST(ElemTypeTraitsTest, is_rvv_floating_point) {
  EXPECT_EQ((rvv::is_rvv_floating_point<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kIsRvvFloatingPoint));
}

TYPED_TEST(ElemTypeTraitsTest, is_rvv_unsigned) {
  EXPECT_EQ((rvv::is_rvv_unsigned<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kIsRvvUnsigned));
}

TYPED_TEST(ElemTypeTraitsTest, is_rvv_signed) {
  EXPECT_EQ((rvv::is_rvv_signed<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kIsRvvSigned));
}

TYPED_TEST(ElemTypeTraitsTest, is_rvv_integral) {
  EXPECT_EQ((rvv::is_rvv_integral<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kIsRvvIntegral));
}

TYPED_TEST(ElemTypeTraitsTest, relies_on_unsupported_zvfh) {
  EXPECT_EQ(
      (rvv::relies_on_unsupported_zvfh<typename TypeParam::ElemType, true>),
      !!(TypeParam::kTrait & ElemTypeTraits::kReliesUnsupportedZvfh));
  EXPECT_EQ(
      (rvv::relies_on_unsupported_zvfh<typename TypeParam::ElemType, false>),
      !!(TypeParam::kTrait & ElemTypeTraits::kReliesUnsupportedZvfhmin));
}

TYPED_TEST(ElemTypeTraitsTest, relies_on_unsupported_zve32f) {
  EXPECT_EQ((rvv::relies_on_unsupported_zve32f<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kReliesUnsupportedZve32f));
}

TYPED_TEST(ElemTypeTraitsTest, relies_on_unsupported_zve64d) {
  EXPECT_EQ((rvv::relies_on_unsupported_zve64d<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kReliesUnsupportedZve64d));
}

TYPED_TEST(ElemTypeTraitsTest, relies_on_unsupported_zve64x) {
  EXPECT_EQ((rvv::relies_on_unsupported_zve64x<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kReliesUnsupportedZve64x));
}

TYPED_TEST(ElemTypeTraitsTest, is_supported_rvv_elem_type) {
  EXPECT_EQ(
      (rvv::is_supported_rvv_elem_type<typename TypeParam::ElemType, true>),
      !!(TypeParam::kTrait & ElemTypeTraits::kIsSupportedRvvElemTypeNeedZvfh));
  EXPECT_EQ(
      (rvv::is_supported_rvv_elem_type<typename TypeParam::ElemType, false>),
      !!(TypeParam::kTrait & ElemTypeTraits::kIsSupportedRvvElemType));
}

TYPED_TEST(ElemTypeTraitsTest, is_supported_rvv_integral) {
  EXPECT_EQ((rvv::is_supported_rvv_integral<typename TypeParam::ElemType>),
            !!(TypeParam::kTrait & ElemTypeTraits::kIsSupportedRvvIntegral));
}

TYPED_TEST(ElemTypeTraitsTest, is_supported_rvv_floating_point) {
  EXPECT_EQ((rvv::is_supported_rvv_floating_point<typename TypeParam::ElemType,
                                                  true>),
            !!(TypeParam::kTrait &
               ElemTypeTraits::kIsSupportedRvvFloatingPointNeedZvfh));
  EXPECT_EQ(
      (rvv::is_supported_rvv_floating_point<typename TypeParam::ElemType,
                                            false>),
      !!(TypeParam::kTrait & ElemTypeTraits::kIsSupportedRvvFloatingPoint));
}

enum RatioTypeTraits {
  kIsSupportedRatio = 1,
  kReliesUnsupportedElen64 = 2,
};

template <typename Config>
class RatioTypeTraitsTest : public ::testing::Test {};

template <size_t kRatio, RatioTypeTraits kTrait_>
class RatioTypeTraitsConfig {
 public:
  static constexpr size_t kRatio_ = kRatio;
  static constexpr RatioTypeTraits kTrait = kTrait_;
};

using RatioTypeTraitsTestConfigs = ::testing::Types<
    RatioTypeTraitsConfig<1, static_cast<RatioTypeTraits>(kIsSupportedRatio)>,
    RatioTypeTraitsConfig<2, static_cast<RatioTypeTraits>(kIsSupportedRatio)>,
    RatioTypeTraitsConfig<4, static_cast<RatioTypeTraits>(kIsSupportedRatio)>,
    RatioTypeTraitsConfig<8, static_cast<RatioTypeTraits>(kIsSupportedRatio)>,
    RatioTypeTraitsConfig<16, static_cast<RatioTypeTraits>(kIsSupportedRatio)>,
    RatioTypeTraitsConfig<32, static_cast<RatioTypeTraits>(kIsSupportedRatio)>,
    RatioTypeTraitsConfig<33, static_cast<RatioTypeTraits>(0)>,
    RatioTypeTraitsConfig<64, static_cast<RatioTypeTraits>(
                                  HAS_ELEN64 ? kIsSupportedRatio
                                             : kReliesUnsupportedElen64)>,
    RatioTypeTraitsConfig<128, static_cast<RatioTypeTraits>(0)>>;

TYPED_TEST_SUITE(RatioTypeTraitsTest, RatioTypeTraitsTestConfigs);

TYPED_TEST(RatioTypeTraitsTest, is_supported_ratio) {
  EXPECT_EQ((rvv::is_supported_ratio<TypeParam::kRatio_>),
            !!(TypeParam::kTrait & RatioTypeTraits::kIsSupportedRatio));
}

TYPED_TEST(RatioTypeTraitsTest, relies_on_unsupported_elen) {
  EXPECT_EQ((rvv::relies_on_unsupported_elen64<TypeParam::kRatio_>),
            !!(TypeParam::kTrait & RatioTypeTraits::kReliesUnsupportedElen64));
}
