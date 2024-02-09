#ifndef MACROS_H_
#define MACROS_H_

#include <macros/for_each.h>
#include <macros/op_test_base.h>
#include <macros/type.h>

#define FP_TEST(base_macro, test_macro, name, ratio, short_name, lmul)        \
  base_macro(test_macro, name, name<>, ratio, short_name, lmul);              \
  base_macro(test_macro, name##_rne, name<rvv::FRM::kRNE>, ratio, short_name, \
             lmul);                                                           \
  base_macro(test_macro, name##_rtz, name<rvv::FRM::kRTZ>, ratio, short_name, \
             lmul);                                                           \
  base_macro(test_macro, name##_rdn, name<rvv::FRM::kRDN>, ratio, short_name, \
             lmul);                                                           \
  base_macro(test_macro, name##_rup, name<rvv::FRM::kRUP>, ratio, short_name, \
             lmul);                                                           \
  base_macro(test_macro, name##_rmm, name<rvv::FRM::kRMM>, ratio, short_name, \
             lmul)

#endif  // MACROS_H_
