// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fixed.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fixed.h>
#include <rvv/policy/tu/fixed.h>
#include <rvv/policy/tumu/fixed.h>

BASE_BIN_OP_TEST(OP_TEST_ALL, vaadd_rdn, vaadd<rvv::VXRM::kRDN>, 8, i8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vaaddu_rne, vaaddu<rvv::VXRM::kRNE>, 8, u8, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vasub_rnu, vasub<rvv::VXRM::kRNU>, 16, i16, m1);
BASE_BIN_OP_TEST(OP_TEST_ALL, vasubu_rod, vasubu<rvv::VXRM::kROD>, 16, u16, m1);
