// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <gtest/gtest.h>
#include <rvv/type.h>

TEST(IsAnyTest, first) { EXPECT_TRUE((rvv::is_any<int, int, float, double>)); }

TEST(IsAnyTest, middle) {
  EXPECT_TRUE((rvv::is_any<float, int, float, double>));
}
TEST(IsAnyTest, last) {
  EXPECT_TRUE((rvv::is_any<double, int, float, double>));
}

TEST(IsAnyTest, non_exist) {
  EXPECT_FALSE((rvv::is_any<char, int, float, double>));
}

#if HAVE_FLOAT16

TEST(IsFloat16Test, float16) { EXPECT_TRUE((rvv::is_float16<rvv::float16_t>)); }

TEST(IsFloat16Test, float32) { EXPECT_FALSE((rvv::is_float16<float>)); }

#endif

TEST(IsFloat32Test, float32) { EXPECT_TRUE((rvv::is_float32<float>)); }

TEST(IsFloat32Test, float64) { EXPECT_FALSE((rvv::is_float32<double>)); }

TEST(IsFloat64Test, float64) { EXPECT_TRUE((rvv::is_float64<double>)); }

TEST(IsFloat64Test, float32) { EXPECT_FALSE((rvv::is_float64<float>)); }

#if HAVE_FLOAT16
TEST(IsRvvFloatingPointTest, float16) {
  EXPECT_TRUE((rvv::is_rvv_floating_point<rvv::float16_t>));
}
#endif

TEST(IsRvvFloatingPointTest, float32) {
  EXPECT_TRUE((rvv::is_rvv_floating_point<float>));
}

TEST(IsRvvFloatingPointTest, float64) {
  EXPECT_TRUE((rvv::is_rvv_floating_point<double>));
}

TEST(IsRvvFloatingPointTest, int) {
  EXPECT_FALSE((rvv::is_rvv_floating_point<int>));
}

TEST(IsRvvUnsignedTest, uint8) { EXPECT_TRUE((rvv::is_rvv_unsigned<uint8_t>)); }

TEST(IsRvvUnsignedTest, uint16) {
  EXPECT_TRUE((rvv::is_rvv_unsigned<uint16_t>));
}

TEST(IsRvvUnsignedTest, uint32) {
  EXPECT_TRUE((rvv::is_rvv_unsigned<uint32_t>));
}

TEST(IsRvvUnsignedTest, uint64) {
  EXPECT_TRUE((rvv::is_rvv_unsigned<uint64_t>));
}

TEST(IsRvvUnsignedTest, int32) {
  EXPECT_FALSE((rvv::is_rvv_unsigned<int32_t>));
}

TEST(IsRvvUnsignedTest, float) { EXPECT_FALSE((rvv::is_rvv_signed<float>)); }

TEST(IsRvvSignedTest, int8) { EXPECT_TRUE((rvv::is_rvv_signed<int8_t>)); }

TEST(IsRvvSignedTest, int16) { EXPECT_TRUE((rvv::is_rvv_signed<int16_t>)); }

TEST(IsRvvSignedTest, int32) { EXPECT_TRUE((rvv::is_rvv_signed<int32_t>)); }

TEST(IsRvvSignedTest, int64) { EXPECT_TRUE((rvv::is_rvv_signed<int64_t>)); }

TEST(IsRvvSignedTest, uint8) { EXPECT_FALSE((rvv::is_rvv_signed<uint8_t>)); }

TEST(IsRvvSignedTest, float) { EXPECT_FALSE((rvv::is_rvv_signed<float>)); }

TEST(IsRvvIntegralTest, int32) { EXPECT_TRUE((rvv::is_rvv_integral<int32_t>)); }

TEST(IsRvvIntegralTest, uint8) { EXPECT_TRUE((rvv::is_rvv_integral<uint8_t>)); }

#if defined(__riscv_zvfh)
TEST(ReliesUnsupportedZvfhTest, float16) {
  EXPECT_FALSE((rvv::relies_on_unsupported_zvfh<rvv::float16_t, false>));
  EXPECT_FALSE((rvv::relies_on_unsupported_zvfh<rvv::float16_t, true>));
}
#elif defined(__riscv_zvfhmin)
TEST(ReliesUnsupportedZvfhTest, float16) {
  EXPECT_FALSE((rvv::relies_on_unsupported_zvfh<rvv::float16_t, false>));
  EXPECT_TRUE((rvv::relies_on_unsupported_zvfh<rvv::float16_t, true>));
}
#elif HAVE_FLOAT16
TEST(ReliesUnsupportedZvfhTest, float16) {
  EXPECT_TRUE((rvv::relies_on_unsupported_zvfh<rvv::float16_t, false>));
  EXPECT_TRUE((rvv::relies_on_unsupported_zvfh<rvv::float16_t, true>));
}
#endif

TEST(ReliesUnsupportedZvfhTest, float32) {
  EXPECT_FALSE((rvv::relies_on_unsupported_zvfh<float, false>));
  EXPECT_FALSE((rvv::relies_on_unsupported_zvfh<float, true>));
}

#if defined(__riscv_zve32f)
TEST(ReliesUnsupportedZve32fTest, float32) {
  EXPECT_FALSE((rvv::relies_on_unsupported_zve32f<float>));
}
#else
TEST(ReliesUnsupportedZve32fTest, float32) {
  EXPECT_TRUE((rvv::relies_on_unsupported_zve32f<float>));
}
#endif

#if defined(__riscv_zve64d)
TEST(ReliesUnsupportedZve64dTest, float64) {
  EXPECT_FALSE((rvv::relies_on_unsupported_zve64d<double>));
}
#else
TEST(ReliesUnsupportedZve64dTest, float64) {
  EXPECT_TRUE((rvv::relies_on_unsupported_zve64d<double>));
}
#endif

#if defined(__riscv_zve64x)
TEST(ReliesUnsupportedZve64xTest, int64) {
  EXPECT_FALSE((rvv::relies_on_unsupported_zve64x<int64_t>));
}
TEST(ReliesUnsupportedZve64xTest, uint64) {
  EXPECT_FALSE((rvv::relies_on_unsupported_zve64x<uint64_t>));
}
#else
TEST(ReliesUnsupportedZve64xTest, int64) {
  EXPECT_TRUE((rvv::relies_on_unsupported_zve64x<int64_t>));
}
TEST(ReliesUnsupportedZve64xTest, uint64) {
  EXPECT_TRUE((rvv::relies_on_unsupported_zve64x<uint64_t>));
}
#endif

#if HAVE_FLOAT16
#if defined(__riscv_zvfh)
TEST(IsSupportedRvvElemTypeTest, float16) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<rvv::float16_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<rvv::float16_t, false>));
}
#elif defined(__riscv_zvfhmin)
TEST(IsSupportedRvvElemTypeTest, float16) {
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<rvv::float16_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<rvv::float16_t, false>));
}
#else
TEST(IsSupportedRvvElemTypeTest, float16) {
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<rvv::float16_t, true>));
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<rvv::float16_t, false>));
}
#endif
#endif

#if defined(__riscv_zve32f)
TEST(IsSupportedRvvElemTypeTest, float32) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<float, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<float, false>));
}
#else
TEST(IsSupportedRvvElemTypeTest, float32) {
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<float, true>));
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<float, false>));
}
#endif

#if defined(__riscv_zve64d)
TEST(IsSupportedRvvElemTypeTest, float64) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<double, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<double, false>));
}
#else
TEST(IsSupportedRvvElemTypeTest, float64) {
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<double, true>));
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<double, false>));
}
#endif

TEST(IsSupportedRvvElemTypeTest, uint8_t) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<uint8_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<uint8_t, false>));
}

TEST(IsSupportedRvvElemTypeTest, uint16_t) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<uint16_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<uint16_t, false>));
}

TEST(IsSupportedRvvElemTypeTest, uint32_t) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<uint32_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<uint32_t, false>));
}

#if defined(__riscv_zve64x)
TEST(IsSupportedRvvElemTypeTest, uint64_t) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<uint64_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<uint64_t, false>));
}
#else
TEST(IsSupportedRvvElemTypeTest, uint64_t) {
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<uint64_t, true>));
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<uint64_t, false>));
}
#endif

TEST(IsSupportedRvvElemTypeTest, int8_t) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<int8_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<int8_t, false>));
}

TEST(IsSupportedRvvElemTypeTest, int16_t) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<int16_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<int16_t, false>));
}

TEST(IsSupportedRvvElemTypeTest, int32_t) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<int32_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<int32_t, false>));
}

#if defined(__riscv_zve64x)
TEST(IsSupportedRvvElemTypeTest, int64_t) {
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<int64_t, true>));
  EXPECT_TRUE((rvv::is_supported_rvv_elem_type<int64_t, false>));
}
#else
TEST(IsSupportedRvvElemTypeTest, int64_t) {
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<int64_t, true>));
  EXPECT_FALSE((rvv::is_supported_rvv_elem_type<int64_t, false>));
}
#endif

#if __riscv_v_elen == 64
TEST(ReliesUnsupportedElenTest, 64) {
  EXPECT_FALSE((rvv::relies_on_unsupported_elen<64>));
  EXPECT_FALSE((rvv::relies_on_unsupported_elen<32>));
}
#elif __riscv_v_elen == 32
TEST(ReliesUnsupportedElenTest, 32) {
  EXPECT_TRUE((rvv::relies_on_unsupported_elen<64>));
  EXPECT_FALSE((rvv::relies_on_unsupported_elen<32>));
}
#endif

#if __riscv_v_elen == 64
TEST(IsSupportedRatioTest, all) {
  EXPECT_TRUE((rvv::is_supported_ratio<1>));
  EXPECT_TRUE((rvv::is_supported_ratio<2>));
  EXPECT_TRUE((rvv::is_supported_ratio<4>));
  EXPECT_TRUE((rvv::is_supported_ratio<8>));
  EXPECT_TRUE((rvv::is_supported_ratio<16>));
  EXPECT_TRUE((rvv::is_supported_ratio<32>));
  EXPECT_TRUE((rvv::is_supported_ratio<64>));
}
#elif __riscv_v_elen == 32
TEST(IsSupportedRatioTest, all) {
  EXPECT_TRUE((rvv::is_supported_ratio<1>));
  EXPECT_TRUE((rvv::is_supported_ratio<2>));
  EXPECT_TRUE((rvv::is_supported_ratio<4>));
  EXPECT_TRUE((rvv::is_supported_ratio<8>));
  EXPECT_TRUE((rvv::is_supported_ratio<16>));
  EXPECT_TRUE((rvv::is_supported_ratio<32>));
  EXPECT_FALSE((rvv::is_supported_ratio<64>));
}
#endif
