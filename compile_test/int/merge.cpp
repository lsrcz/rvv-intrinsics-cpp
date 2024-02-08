// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

VXM_V_TEST(vmerge, 2, i16, m8)
VXM_V_TEST(vmerge, 8, u16, m2)
VVM_V_TEST(vmerge, 2, i16, m8)
VVM_V_TEST(vmerge, 8, u16, m2)
