// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include "rvv/conversion.h"

#include <gtest/gtest.h>
#include <rvv/config.h>
#include <rvv/type.h>

#include <cstddef>

template <typename Config>
class WideningTest : public ::testing::Test {};

template <typename Narrow_, typename Wide_, bool kWidenable_,
          bool kNeedZvfh_ = false>
class WideningConfig {
 public:
  using Narrow = Narrow_;
  using Wide = Wide_;
  static constexpr bool kWidenable = kWidenable_;
  static constexpr bool kNeedZvfh = kNeedZvfh_;
};

using WideningConfigs =
    ::testing::Types<WideningConfig<int8_t, int16_t, true>,
                     WideningConfig<int16_t, int32_t, true>,
                     WideningConfig<uint8_t, uint16_t, true>,
                     WideningConfig<uint16_t, uint32_t, true>,
#if HAS_ZVE64X
                     WideningConfig<int32_t, int64_t, true>,
                     WideningConfig<uint32_t, uint64_t, true>,
                     WideningConfig<int64_t, void, false>,
                     WideningConfig<uint64_t, void, false>,
#else
                     WideningConfig<int32_t, void, false>,
                     WideningConfig<uint32_t, void, false>,
#endif
#if HAS_ZVE64D && HAS_ZVE32F
                     WideningConfig<float, double, true>,
#else
                     WideningConfig<float, void, false>,
#endif
#if HAS_ZVE32F && HAS_ZVFHMIN
                     WideningConfig<rvv::float16_t, float, true>,

#else
                     WideningConfig<rvv::float16_t, void, false>,
#endif
#if HAS_ZVE32F && HAS_ZVFH
                     WideningConfig<rvv::float16_t, float, true, true>,
#else
                     WideningConfig<rvv::float16_t, void, false, true>,
#endif
                     WideningConfig<vint8m1_t, vint16m2_t, true>,
#if HAS_ZVE64X
                     WideningConfig<vuint32m2_t, vuint64m4_t, true>,
                     WideningConfig<vuint64m4_t, void, false>,
#else
                     WideningConfig<vuint32m2_t, void, false>,
#endif
#if HAS_ZVE32F && HAS_ZVE64D
                     WideningConfig<vfloat32m1_t, vfloat64m2_t, true>,
#else
                     WideningConfig<vfloat32m1_t, void, false>,
#endif
                     WideningConfig<vint8m8_t, void, false>>;

TYPED_TEST_SUITE(WideningTest, WideningConfigs);

TYPED_TEST(WideningTest, widening) {
  EXPECT_TRUE(
      (rvv::Widenable<typename TypeParam::Narrow, TypeParam::kNeedZvfh> ==
       TypeParam::kWidenable));
  if constexpr (rvv::Widenable<typename TypeParam::Narrow,
                               TypeParam::kNeedZvfh>) {
    EXPECT_TRUE((std::is_same_v<
                 rvv::widen_t<typename TypeParam::Narrow, TypeParam::kNeedZvfh>,
                 typename TypeParam::Wide>));
  }
}

template <typename Config>
class NarrowingTest : public ::testing::Test {};

template <typename Narrow_, typename Wide_, bool kNarrowable_,
          bool kNeedZvfh_ = false>
class NarrowingConfig {
 public:
  using Narrow = Narrow_;
  using Wide = Wide_;
  static constexpr bool kNarrowable = kNarrowable_;
  static constexpr bool kNeedZvfh = kNeedZvfh_;
};

using NarrowingConfigs =
    ::testing::Types<NarrowingConfig<int8_t, int16_t, true>,
                     NarrowingConfig<int16_t, int32_t, true>,
                     NarrowingConfig<uint8_t, uint16_t, true>,
                     NarrowingConfig<uint16_t, uint32_t, true>,
#if HAS_ZVE64X
                     NarrowingConfig<int32_t, int64_t, true>,
                     NarrowingConfig<uint32_t, uint64_t, true>,
#endif
                     NarrowingConfig<void, int8_t, false>,
                     NarrowingConfig<void, uint8_t, false>,
#if HAS_ZVE64D && HAS_ZVE32F
                     NarrowingConfig<float, double, true>,
#else
                     NarrowingConfig<void, double, false>,
#endif
#if HAS_ZVE32F && HAS_ZVFHMIN
                     NarrowingConfig<rvv::float16_t, float, true>,

#else
                     NarrowingConfig<void, float, false>,
#endif
#if HAS_ZVE32F && HAS_ZVFH
                     NarrowingConfig<rvv::float16_t, float, true, true>,
#else
                     NarrowingConfig<void, float, false, true>,
#endif
                     NarrowingConfig<vint8m1_t, vint16m2_t, true>,
#if HAS_ZVE64X
                     NarrowingConfig<vuint32m2_t, vuint64m4_t, true>,
#endif
#if HAS_ZVE32F && HAS_ZVE64D
                     NarrowingConfig<vfloat32m1_t, vfloat64m2_t, true>,
#else
                     NarrowingConfig<void, vfloat64m2_t, false>,
#endif
                     NarrowingConfig<void, vint8m8_t, false>>;

TYPED_TEST_SUITE(NarrowingTest, NarrowingConfigs);

TYPED_TEST(NarrowingTest, narrowing) {
  EXPECT_TRUE(
      (rvv::Narrowable<typename TypeParam::Wide, TypeParam::kNeedZvfh> ==
       TypeParam::kNarrowable));
  if constexpr (rvv::Narrowable<typename TypeParam::Wide,
                                TypeParam::kNeedZvfh>) {
    EXPECT_TRUE((std::is_same_v<
                 rvv::narrow_t<typename TypeParam::Wide, TypeParam::kNeedZvfh>,
                 typename TypeParam::Narrow>));
  }
}

template <typename Config>
class WideningNTest : public ::testing::Test {};

template <typename Narrow_, typename Wide_, size_t kN_, bool kWidenable_,
          bool kNeedZvfh_ = false>
class WideningNConfig {
 public:
  using Narrow = Narrow_;
  using Wide = Wide_;
  static constexpr size_t kN = kN_;
  static constexpr bool kWidenable = kWidenable_;
  static constexpr bool kNeedZvfh = kNeedZvfh_;
};

using WideningNConfigs = ::testing::Types<
    WideningNConfig<int8_t, int16_t, 2, true>,
    WideningNConfig<uint8_t, uint16_t, 2, true>,
    WideningNConfig<int8_t, int32_t, 4, true>,
    WideningNConfig<uint8_t, uint32_t, 4, true>,
    WideningNConfig<int16_t, int32_t, 2, true>,
    WideningNConfig<uint16_t, uint32_t, 2, true>,
    WideningNConfig<int16_t, void, 8, false>,
    WideningNConfig<uint16_t, void, 8, false>,
    WideningNConfig<int32_t, void, 4, false>,
    WideningNConfig<uint32_t, void, 4, false>,
    WideningNConfig<int32_t, void, 8, false>,
    WideningNConfig<uint32_t, void, 8, false>,
    WideningNConfig<int64_t, void, 2, false>,
    WideningNConfig<uint64_t, void, 2, false>,
    WideningNConfig<int64_t, void, 4, false>,
    WideningNConfig<uint64_t, void, 4, false>,
    WideningNConfig<int64_t, void, 8, false>,
    WideningNConfig<uint64_t, void, 8, false>,
#if HAS_ZVE64X
    WideningNConfig<int8_t, int64_t, 8, true>,
    WideningNConfig<uint8_t, uint64_t, 8, true>,
    WideningNConfig<int16_t, int64_t, 4, true>,
    WideningNConfig<uint16_t, uint64_t, 4, true>,
    WideningNConfig<int32_t, int64_t, 2, true>,
    WideningNConfig<uint32_t, uint64_t, 2, true>,
#else
    WideningNConfig<int8_t, void, 8, false>,
    WideningNConfig<uint8_t, void, 8, false>,
    WideningNConfig<int16_t, void, 4, false>,
    WideningNConfig<uint16_t, void, 4, false>,
    WideningNConfig<int32_t, void, 2, false>,
    WideningNConfig<uint32_t, void, 2, false>,
#endif
#if HAS_ZVE32F && HAS_ZVE64D
    WideningNConfig<float, double, 2, true>,
#else
    WideningNConfig<float, void, 2, false>,
#endif
    WideningNConfig<vint8m1_t, vint16m2_t, 2, true>,
    WideningNConfig<vint8m1_t, vint32m4_t, 4, true>,
#if HAS_ZVE64X
    WideningNConfig<vuint8m1_t, vuint64m8_t, 8, true>,
    WideningNConfig<vuint64m4_t, void, 2, false>,
#else
    WideningNConfig<vuint8m1_t, void, 8, false>,
#endif
#if HAS_ZVE32F && HAS_ZVE64D
    WideningNConfig<vfloat32m1_t, vfloat64m2_t, 2, true>,
#else
    WideningNConfig<vfloat32m1_t, void, 2, false>,
#endif
#if HAS_ZVFHMIN && HAS_ZVE64D
    WideningNConfig<vfloat16mf2_t, vfloat64m2_t, 4, true>,
#else
    WideningNConfig<vfloat16mf2_t, void, 4, false>,
#endif
#if HAS_ZVFH && HAS_ZVE64D
    WideningNConfig<vfloat16mf2_t, vfloat64m2_t, 4, true, true>,
#else
    WideningNConfig<vfloat16mf2_t, void, 4, false, true>,
#endif
    WideningNConfig<vint8m8_t, void, 2, false>>;

TYPED_TEST_SUITE(WideningNTest, WideningNConfigs);

TYPED_TEST(WideningNTest, widening_n) {
  EXPECT_TRUE((rvv::WidenableN<TypeParam::kN, typename TypeParam::Narrow,
                               TypeParam::kNeedZvfh> == TypeParam::kWidenable));
  if constexpr (rvv::WidenableN<TypeParam::kN, typename TypeParam::Narrow,
                                TypeParam::kNeedZvfh>) {
    EXPECT_TRUE((
        std::is_same_v<rvv::widen_n_t<TypeParam::kN, typename TypeParam::Narrow,
                                      TypeParam::kNeedZvfh>,
                       typename TypeParam::Wide>));
  }
}

template <typename Config>
class ToSignedTest : public ::testing::Test {};

template <typename T_, typename Signed_, bool kConvertibleToSigned_,
          bool kNeedZvfh_ = false>
class ToSignedConfig {
 public:
  using T = T_;
  using Signed = Signed_;
  constexpr static bool kConvertibleToSigned = kConvertibleToSigned_;
  constexpr static bool kNeedZvfh = kNeedZvfh_;
};

using ToSignedConfigs = ::testing::Types<
#if HAS_ZVE64X
    ToSignedConfig<int64_t, int64_t, true>,
    ToSignedConfig<uint64_t, int64_t, true>,
#else
    ToSignedConfig<int64_t, void, false>, ToSignedConfig<uint64_t, void, false>,
#endif
#if HAS_ZVFHMIN
    ToSignedConfig<rvv::float16_t, int16_t, true>,
#else
    ToSignedConfig<rvv::float16_t, void, false>,
#endif
#if HAS_ZVFH
    ToSignedConfig<rvv::float16_t, int16_t, true, true>,
#else
    ToSignedConfig<rvv::float16_t, void, false, true>,
#endif
#if HAS_ZVE32F
    ToSignedConfig<rvv::float32_t, int32_t, true>,
#else
    ToSignedConfig<rvv::float32_t, void, false>,
#endif
#if HAS_ZVE64D
    ToSignedConfig<rvv::float64_t, int64_t, true>,
#else
    ToSignedConfig<rvv::float64_t, void, false>,
#endif
    ToSignedConfig<int8_t, int8_t, true>, ToSignedConfig<uint8_t, int8_t, true>,
    ToSignedConfig<int16_t, int16_t, true>,
    ToSignedConfig<uint16_t, int16_t, true>,
    ToSignedConfig<int32_t, int32_t, true>,
    ToSignedConfig<uint32_t, int32_t, true>, ToSignedConfig<void, void, false>,
    ToSignedConfig<vuint8m1_t, vint8m1_t, true>>;

TYPED_TEST_SUITE(ToSignedTest, ToSignedConfigs);

TYPED_TEST(ToSignedTest, to_signed) {
  EXPECT_TRUE(
      (rvv::ConvertibleToSigned<typename TypeParam::T, TypeParam::kNeedZvfh> ==
       TypeParam::kConvertibleToSigned));
  if constexpr (TypeParam::kConvertibleToSigned) {
    EXPECT_TRUE((std::is_same_v<
                 rvv::to_signed_t<typename TypeParam::T, TypeParam::kNeedZvfh>,
                 typename TypeParam::Signed>));
  }
}

template <typename Config>
class ToUnsignedTest : public ::testing::Test {};

template <typename T_, typename Unsigned_, bool kConvertibleToUnsigned_,
          bool kNeedZvfh_ = false>
class ToUnsignedConfig {
 public:
  using T = T_;
  using Unsigned = Unsigned_;
  constexpr static bool kConvertibleToUnsigned = kConvertibleToUnsigned_;
  constexpr static bool kNeedZvfh = kNeedZvfh_;
};

using ToUnsignedConfigs = ::testing::Types<
#if HAS_ZVE64X
    ToUnsignedConfig<int64_t, uint64_t, true>,
    ToUnsignedConfig<uint64_t, uint64_t, true>,
#else
    ToUnsignedConfig<int64_t, void, false>,
    ToUnsignedConfig<uint64_t, void, false>,
#endif
#if HAS_ZVFHMIN
    ToUnsignedConfig<rvv::float16_t, uint16_t, true>,
#else
    ToUnsignedConfig<rvv::float16_t, void, false>,
#endif
#if HAS_ZVFH
    ToUnsignedConfig<rvv::float16_t, uint16_t, true, true>,
#else
    ToUnsignedConfig<rvv::float16_t, void, false, true>,
#endif
#if HAS_ZVE32F
    ToUnsignedConfig<rvv::float32_t, uint32_t, true>,
#else
    ToUnsignedConfig<rvv::float32_t, void, false>,
#endif
#if HAS_ZVE64D
    ToUnsignedConfig<rvv::float64_t, uint64_t, true>,
#else
    ToUnsignedConfig<rvv::float64_t, void, false>,
#endif
    ToUnsignedConfig<int8_t, uint8_t, true>,
    ToUnsignedConfig<uint8_t, uint8_t, true>,
    ToUnsignedConfig<int16_t, uint16_t, true>,
    ToUnsignedConfig<uint16_t, uint16_t, true>,
    ToUnsignedConfig<int32_t, uint32_t, true>,
    ToUnsignedConfig<uint32_t, uint32_t, true>,
    ToUnsignedConfig<void, void, false>,
    ToUnsignedConfig<vuint8m1_t, vuint8m1_t, true>>;

TYPED_TEST_SUITE(ToUnsignedTest, ToUnsignedConfigs);

TYPED_TEST(ToUnsignedTest, to_unsigned) {
  EXPECT_TRUE((
      rvv::ConvertibleToUnsigned<typename TypeParam::T, TypeParam::kNeedZvfh> ==
      TypeParam::kConvertibleToUnsigned));
  if constexpr (TypeParam::kConvertibleToUnsigned) {
    EXPECT_TRUE(
        (std::is_same_v<
            rvv::to_unsigned_t<typename TypeParam::T, TypeParam::kNeedZvfh>,
            typename TypeParam::Unsigned>));
  }
}

template <typename Config>
class ToFloatingPointTest : public ::testing::Test {};

template <typename T_, typename Unsigned_, bool kConvertibleToFloatingPoint_,
          bool kNeedZvfh_ = false>
class ToFloatingPointConfig {
 public:
  using T = T_;
  using Unsigned = Unsigned_;
  constexpr static bool kConvertibleToFloatingPoint =
      kConvertibleToFloatingPoint_;
  constexpr static bool kNeedZvfh = kNeedZvfh_;
};

using ToFloatingPointConfigs = ::testing::Types<
#if HAS_ZVFHMIN
    ToFloatingPointConfig<rvv::float16_t, rvv::float16_t, true>,
    ToFloatingPointConfig<int16_t, rvv::float16_t, true>,
    ToFloatingPointConfig<uint16_t, rvv::float16_t, true>,
    ToFloatingPointConfig<vint16m1_t, vfloat16m1_t, true>,
    ToFloatingPointConfig<vuint16m1_t, vfloat16m1_t, true>,
#else
    ToFloatingPointConfig<rvv::float16_t, void, false>,
    ToFloatingPointConfig<int16_t, void, false>,
    ToFloatingPointConfig<uint16_t, void, false>,
    ToFloatingPointConfig<vint16m1_t, void, false>,
    ToFloatingPointConfig<vuint16m1_t, void, false>,
#endif
#if HAS_ZVFH
    ToFloatingPointConfig<rvv::float16_t, rvv::float16_t, true, true>,
    ToFloatingPointConfig<int16_t, rvv::float16_t, true, true>,
    ToFloatingPointConfig<uint16_t, rvv::float16_t, true, true>,
    ToFloatingPointConfig<vint16m1_t, vfloat16m1_t, true, true>,
    ToFloatingPointConfig<vuint16m1_t, vfloat16m1_t, true, true>,
#else
    ToFloatingPointConfig<rvv::float16_t, void, false, true>,
    ToFloatingPointConfig<int16_t, void, false, true>,
    ToFloatingPointConfig<uint16_t, void, false, true>,
    ToFloatingPointConfig<vint16m1_t, void, false, true>,
    ToFloatingPointConfig<vuint16m1_t, void, false, true>,
#endif
#if HAS_ZVE32F
    ToFloatingPointConfig<rvv::float32_t, rvv::float32_t, true>,
    ToFloatingPointConfig<int32_t, rvv::float32_t, true>,
    ToFloatingPointConfig<uint32_t, rvv::float32_t, true>,
    ToFloatingPointConfig<vint32m1_t, vfloat32m1_t, true>,
    ToFloatingPointConfig<vuint32m1_t, vfloat32m1_t, true>,
#else
    ToFloatingPointConfig<rvv::float32_t, void, false>,
    ToFloatingPointConfig<int32_t, void, false>,
    ToFloatingPointConfig<uint32_t, void, false>,
    ToFloatingPointConfig<vint32m1_t, void, false>,
    ToFloatingPointConfig<vuint32m1_t, void, false>,
#endif
#if HAS_ZVE64D && HAS_ZVE64X
    ToFloatingPointConfig<rvv::float64_t, rvv::float64_t, true>,
    ToFloatingPointConfig<int64_t, rvv::float64_t, true>,
    ToFloatingPointConfig<uint64_t, rvv::float64_t, true>,
    ToFloatingPointConfig<vint64m1_t, vfloat64m1_t, true>,
    ToFloatingPointConfig<vuint64m1_t, vfloat64m1_t, true>,
#else
    ToFloatingPointConfig<rvv::float64_t, void, false>,
    ToFloatingPointConfig<int64_t, void, false>,
    ToFloatingPointConfig<uint64_t, void, false>,
    ToFloatingPointConfig<vint64m1_t, void, false>,
    ToFloatingPointConfig<vuint64m1_t, void, false>,
#endif
    ToFloatingPointConfig<int8_t, void, false>,
    ToFloatingPointConfig<uint8_t, void, false>,
    ToFloatingPointConfig<void, void, false>>;

TYPED_TEST_SUITE(ToFloatingPointTest, ToFloatingPointConfigs);

TYPED_TEST(ToFloatingPointTest, to_float_t) {
  EXPECT_TRUE((rvv::ConvertibleToFloatingPoint<typename TypeParam::T,
                                               TypeParam::kNeedZvfh> ==
               TypeParam::kConvertibleToFloatingPoint));
  if constexpr (TypeParam::kConvertibleToFloatingPoint) {
    EXPECT_TRUE((std::is_same_v<
                 rvv::to_float_t<typename TypeParam::T, TypeParam::kNeedZvfh>,
                 typename TypeParam::Unsigned>));
  }
}
