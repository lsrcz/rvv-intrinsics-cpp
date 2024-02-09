// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/fixed.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/fixed.h>
#include <rvv/policy/tu/fixed.h>
#include <rvv/policy/tumu/fixed.h>

BASE_BIN_OP_TEST(OP_TEST_ALL, vsmul_rdn, vsmul<rvv::VXRM::kRDN>, 8, i8, m1);
