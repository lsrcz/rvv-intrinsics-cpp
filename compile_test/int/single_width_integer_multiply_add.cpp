// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#include <macros.h>
#include <rvv/int.h>
#include <rvv/misc.h>
#include <rvv/policy/mu/int.h>
#include <rvv/policy/tu/int.h>
#include <rvv/policy/tumu/int.h>

FMA_OP_TEST(vmadd, 4, i8, m2);
FMA_OP_TEST(vnmsub, 8, i8, m1);
FMA_OP_TEST(vmadd, 16, u16, m1);
FMA_OP_TEST(vnmsac, 32, u16, mf2);
