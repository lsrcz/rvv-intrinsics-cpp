#ifndef MACROS_OP_TEST_BASE_H_
#define MACROS_OP_TEST_BASE_H_
#include <macros/for_each.h>
#include <macros/type.h>

#define ARG_TYPE0(type, name) type
#define ARG_NAME0(type, name) name
#define ARG_PAIR0(type, name) type name

#define ARG_TYPE(p) ARG_TYPE0 p
#define ARG_NAME(p) ARG_NAME0 p
#define ARG_PAIR(p) ARG_PAIR0 p

#define OP_TEST(name, rvv_name, mask_type, ret_type, ...)       \
  ret_type name(FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) {         \
    return rvv::rvv_name(FOR_EACH_LIST(ARG_NAME, __VA_ARGS__)); \
  }
#define OP_TEST_M(name, rvv_name, mask_type, ret_type, ...)               \
  ret_type name##_m(mask_type vm, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::rvv_name(vm, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));       \
  }
#define OP_TEST_TU(name, rvv_name, mask_type, ret_type, ...)              \
  ret_type name##_tu(ret_type vd, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::tu::rvv_name(vd, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));   \
  }
#define OP_TEST_TUM(name, rvv_name, mask_type, ret_type, ...)               \
  ret_type name##_tum(mask_type vm, ret_type vd,                            \
                      FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) {               \
    return rvv::tu::rvv_name(vm, vd, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__)); \
  }
#define OP_TEST_MU(name, rvv_name, mask_type, ret_type, ...)                \
  ret_type name##_mu(mask_type vm, ret_type vd,                             \
                     FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) {                \
    return rvv::mu::rvv_name(vm, vd, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__)); \
  }
#define OP_TEST_TUMU(name, rvv_name, mask_type, ret_type, ...)                \
  ret_type name##_tumu(mask_type vm, ret_type vd,                             \
                       FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) {                \
    return rvv::tumu::rvv_name(vm, vd, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__)); \
  }

#define OP_TEST_NO_DEST(name, rvv_name, mask_type, ret_type, ...) \
  ret_type name(FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) {           \
    return rvv::rvv_name(FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));   \
  }
#define OP_TEST_M_NO_DEST(name, rvv_name, mask_type, ret_type, ...)       \
  ret_type name##_m(mask_type vm, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::rvv_name(vm, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));       \
  }
#define OP_TEST_TU_NO_DEST(name, rvv_name, mask_type, ret_type, ...) \
  ret_type name##_tu(FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) {         \
    return rvv::tu::rvv_name(FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));  \
  }
#define OP_TEST_TUM_NO_DEST(name, rvv_name, mask_type, ret_type, ...)       \
  ret_type name##_tum(mask_type vm, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::tu::rvv_name(vm, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));     \
  }
#define OP_TEST_MU_NO_DEST(name, rvv_name, mask_type, ret_type, ...)       \
  ret_type name##_mu(mask_type vm, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::mu::rvv_name(vm, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));    \
  }
#define OP_TEST_TUMU_NO_DEST(name, rvv_name, mask_type, ret_type, ...)       \
  ret_type name##_tumu(mask_type vm, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::tumu::rvv_name(vm, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));    \
  }

#define OP_TEST_ALL(name, rvv_name, mask_type, ret_type, ...)   \
  OP_TEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)     \
  OP_TEST_M(name, rvv_name, mask_type, ret_type, __VA_ARGS__)   \
  OP_TEST_TU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)  \
  OP_TEST_TUM(name, rvv_name, mask_type, ret_type, __VA_ARGS__) \
  OP_TEST_MU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)  \
  OP_TEST_TUMU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)

#define OP_TEST_ALL_NO_DEST(name, rvv_name, mask_type, ret_type, ...)   \
  OP_TEST_NO_DEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)     \
  OP_TEST_M_NO_DEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)   \
  OP_TEST_TU_NO_DEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)  \
  OP_TEST_TUM_NO_DEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__) \
  OP_TEST_MU_NO_DEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)  \
  OP_TEST_TUMU_NO_DEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)

#define OP_TEST_NO_MASK(name, rvv_name, mask_type, ret_type, ...) \
  OP_TEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)       \
  OP_TEST_TU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)

#define OP_TEST_NO_TAIL(name, rvv_name, mask_type, ret_type, ...) \
  OP_TEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)       \
  OP_TEST_M(name, rvv_name, mask_type, ret_type, __VA_ARGS__)     \
  OP_TEST_MU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)

#define BASE_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)  \
  macro(name##_vv_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,     \
        VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
        (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl))

#define BASE_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)  \
  macro(name##_vv_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,     \
        VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
        (C_TYPE_NAME(short_name), rs1), (rvv::vl_t<ratio>, vl))

#define BASE_BIN_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  BASE_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)        \
  BASE_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)

#define BASE_UNARY_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  macro(name##_vx_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,       \
        VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2),   \
        (rvv::vl_t<ratio>, vl))

#define BASE_WIDENING_VV_OP_TEST(macro, name, rvv_name, ratio, short_name,     \
                                 lmul)                                         \
  macro(name##_vv_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,           \
        WIDEN_VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
        (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define BASE_WIDENING_VX_OP_TEST(macro, name, rvv_name, ratio, short_name,     \
                                 lmul)                                         \
  macro(name##_vx_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,           \
        WIDEN_VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
        (C_TYPE_NAME(short_name), vs1), (rvv::vl_t<ratio>, vl));
#define BASE_WIDENING_WV_OP_TEST(macro, name, rvv_name, ratio, short_name, \
                                 lmul)                                     \
  macro(name##_vv_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,       \
        WIDEN_VREG_NAME(short_name, lmul),                                 \
        (WIDEN_VREG_NAME(short_name, lmul), vs2),                          \
        (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define BASE_WIDENING_WX_OP_TEST(macro, name, rvv_name, ratio, short_name, \
                                 lmul)                                     \
  macro(name##_vx_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,       \
        WIDEN_VREG_NAME(short_name, lmul),                                 \
        (WIDEN_VREG_NAME(short_name, lmul), vs2),                          \
        (C_TYPE_NAME(short_name), vs1), (rvv::vl_t<ratio>, vl));
#define BASE_WIDENING_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  BASE_WIDENING_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)    \
  BASE_WIDENING_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)    \
  BASE_WIDENING_WV_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)    \
  BASE_WIDENING_WX_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)

#define BASE_FMA_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  macro(name##_vv_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,        \
        VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vd),     \
        (VREG_NAME(short_name, lmul), vs2),                                 \
        (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define BASE_FMA_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  macro(name##_vv_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,        \
        VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vd),     \
        (C_TYPE_NAME(short_name), rs1), (VREG_NAME(short_name, lmul), vs2), \
        (rvv::vl_t<ratio>, vl));
#define BASE_FMA_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  BASE_FMA_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)    \
  BASE_FMA_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)

#define BASE_WIDENING_FMA_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, \
                                     lmul)                                     \
  macro(name##_vv_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,           \
        WIDEN_VREG_NAME(short_name, lmul),                                     \
        (WIDEN_VREG_NAME(short_name, lmul), vd),                               \
        (VREG_NAME(short_name, lmul), vs2),                                    \
        (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define BASE_WIDENING_FMA_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, \
                                     lmul)                                     \
  macro(name##_vx_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,           \
        WIDEN_VREG_NAME(short_name, lmul),                                     \
        (WIDEN_VREG_NAME(short_name, lmul), vd),                               \
        (C_TYPE_NAME(short_name), rs1), (VREG_NAME(short_name, lmul), vs2),    \
        (rvv::vl_t<ratio>, vl));
#define BASE_WIDENING_FMA_OP_TEST(macro, name, rvv_name, ratio, short_name,    \
                                  lmul)                                        \
  BASE_WIDENING_FMA_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  BASE_WIDENING_FMA_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)

#define BASE_VXM_V_TEST(macro, name, rvv_name, ratio, short_name, lmul)  \
  macro(name##_vxm_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,    \
        VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
        (C_TYPE_NAME(short_name), rs1), (rvv::vmask_t<ratio>, v0),       \
        (rvv::vl_t<ratio>, vl));
#define BASE_VVM_V_TEST(macro, name, rvv_name, ratio, short_name, lmul)  \
  macro(name##_vxm_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,    \
        VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
        (VREG_NAME(short_name, lmul), vs1), (rvv::vmask_t<ratio>, v0),   \
        (rvv::vl_t<ratio>, vl))

#define BASE_WITH_CARRY_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  BASE_VXM_V_TEST(macro, name, rvv_name, ratio, short_name, lmul)            \
  BASE_VVM_V_TEST(macro, name, rvv_name, ratio, short_name, lmul)

#define BASE_COMPARE_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, \
                                lmul)                                     \
  macro(name##_vv_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,      \
        rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2),          \
        (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));

#define BASE_COMPARE_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, \
                                lmul)                                     \
  macro(name##_vx_##short_name##lmul, rvv_name, rvv::vmask_t<ratio>,      \
        rvv::vmask_t<ratio>, (VREG_NAME(short_name, lmul), vs2),          \
        (C_TYPE_NAME(short_name), rs1), (rvv::vl_t<ratio>, vl));

#define BASE_COMPARE_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul) \
  BASE_COMPARE_VV_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)    \
  BASE_COMPARE_VX_OP_TEST(macro, name, rvv_name, ratio, short_name, lmul)

#endif  // MACROS_OP_TEST_BASE_H_
