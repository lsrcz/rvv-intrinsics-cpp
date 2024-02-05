// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <gtest/gtest.h>
#include <rvv/misc.h>

template <typename Config>
class SetVLTest : public testing::Test {};

template <typename E, size_t kRatio_, rvv::LMul kLMul_, size_t kAvl_>
class SetVLConfig {
 public:
  using ElemType = E;
  static constexpr size_t kRatio = kRatio_;
  static constexpr rvv::LMul kLMul = kLMul_;
  static constexpr size_t kAvl = kAvl_;
};

using SetVLConfigs =
    ::testing::Types<SetVLConfig<int8_t, 8, rvv::LMul::kM1, 1>,
                     SetVLConfig<int8_t, 8, rvv::LMul::kM1, 8>,
                     SetVLConfig<int8_t, 8, rvv::LMul::kM1, 16>,
                     SetVLConfig<int8_t, 8, rvv::LMul::kM1, 10000> >;

TYPED_TEST_SUITE(SetVLTest, SetVLConfigs);

TYPED_TEST(SetVLTest, SetVL) {
  auto vl1 = rvv::vsetvl<typename TypeParam::ElemType, TypeParam::kLMul>(
      TypeParam::kAvl);
  auto vl2 = rvv::vsetvl<TypeParam::kRatio>(TypeParam::kAvl);
  auto expected = __riscv_vsetvl_e8m1(TypeParam::kAvl);
  EXPECT_EQ(vl1, expected);
  EXPECT_EQ(vl2, expected);
}

TYPED_TEST(SetVLTest, SetVLMax) {
  auto vl1 = rvv::vsetvlmax<TypeParam::kRatio>();
  auto vl2 = rvv::vsetvlmax<typename TypeParam::ElemType, TypeParam::kLMul>();
  auto expected = __riscv_vsetvlmax_e8m1();
  EXPECT_EQ(vl1, expected);
  EXPECT_EQ(vl2, expected);
}
