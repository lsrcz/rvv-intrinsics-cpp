#ifndef MACROS_H_
#define MACROS_H_

#define PARENS ()

#define EXPAND(...) EXPAND4(EXPAND4(EXPAND4(EXPAND4(__VA_ARGS__))))
#define EXPAND4(...) EXPAND3(EXPAND3(EXPAND3(EXPAND3(__VA_ARGS__))))
#define EXPAND3(...) EXPAND2(EXPAND2(EXPAND2(EXPAND2(__VA_ARGS__))))
#define EXPAND2(...) EXPAND1(EXPAND1(EXPAND1(EXPAND1(__VA_ARGS__))))
#define EXPAND1(...) __VA_ARGS__

#define FOR_EACH_LIST(macro, ...) \
  __VA_OPT__(EXPAND(FOR_EACH_LIST_HELPER(macro, __VA_ARGS__)))
#define FOR_EACH_LIST_HELPER(macro, a1, ...) \
  macro(a1) __VA_OPT__(FOR_EACH_LIST_AGAIN PARENS(macro, __VA_ARGS__))
#define FOR_EACH_LIST_AGAIN() , FOR_EACH_LIST_HELPER

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

#define OP_TEST_ALL(name, rvv_name, mask_type, ret_type, ...)   \
  OP_TEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)     \
  OP_TEST_M(name, rvv_name, mask_type, ret_type, __VA_ARGS__)   \
  OP_TEST_TU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)  \
  OP_TEST_TUM(name, rvv_name, mask_type, ret_type, __VA_ARGS__) \
  OP_TEST_MU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)  \
  OP_TEST_TUMU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)

#define OP_TEST_NO_MASK(name, rvv_name, mask_type, ret_type, ...) \
  OP_TEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)       \
  OP_TEST_TU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)

#define OP_TEST_NO_TAIL(name, rvv_name, mask_type, ret_type, ...) \
  OP_TEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)       \
  OP_TEST_M(name, rvv_name, mask_type, ret_type, __VA_ARGS__)     \
  OP_TEST_MU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)

#define LONG_TYPE_NAME_i8 int8
#define LONG_TYPE_NAME_i16 int16
#define LONG_TYPE_NAME_i32 int32
#define LONG_TYPE_NAME_i64 int64
#define LONG_TYPE_NAME_u8 uint8
#define LONG_TYPE_NAME_u16 uint16
#define LONG_TYPE_NAME_u32 uint32
#define LONG_TYPE_NAME_u64 uint64
#define LONG_TYPE_NAME_f16 float16
#define LONG_TYPE_NAME_f32 float32
#define LONG_TYPE_NAME_f64 float64

#define LONG_TYPE_NAME(short_name) LONG_TYPE_NAME_##short_name
#define C_TYPE_NAME_i8 int8_t
#define C_TYPE_NAME_i16 int16_t
#define C_TYPE_NAME_i32 int32_t
#define C_TYPE_NAME_i64 int64_t
#define C_TYPE_NAME_u8 uint8_t
#define C_TYPE_NAME_u16 uint16_t
#define C_TYPE_NAME_u32 uint32_t
#define C_TYPE_NAME_u64 uint64_t
#define C_TYPE_NAME_f16 rvv::float16_t
#define C_TYPE_NAME_f32 rvv::float32_t
#define C_TYPE_NAME_f64 rvv::float64_t
#define C_TYPE_NAME0(short_name) C_TYPE_NAME_##short_name
#define C_TYPE_NAME(...) C_TYPE_NAME0(__VA_ARGS__)

#define CONCAT(a, b) a##b

#define VREG_NAME_LONG0(long_name, lmul) v##long_name##lmul##_t
#define VREG_NAME_LONG(...) VREG_NAME_LONG0(__VA_ARGS__)

#define VREG_NAME0(short_name, lmul) \
  VREG_NAME_LONG(LONG_TYPE_NAME(short_name), lmul)

#define VREG_NAME(...) VREG_NAME0(__VA_ARGS__)

#define WIDEN_SHORT_NAME_i8 i16
#define WIDEN_SHORT_NAME_i16 i32
#define WIDEN_SHORT_NAME_i32 i64
#define WIDEN_SHORT_NAME_u8 u16
#define WIDEN_SHORT_NAME_u16 u32
#define WIDEN_SHORT_NAME_u32 u64
#define WIDEN_SHORT_NAME_f16 f32
#define WIDEN_SHORT_NAME_f32 f64

#define WIDEN_SHORT_NAME0(short_name) WIDEN_SHORT_NAME_##short_name
#define WIDEN_SHORT_NAME(...) WIDEN_SHORT_NAME0(__VA_ARGS__)

#define WIDEN_SHORT_NAME_2(short_name) WIDEN_SHORT_NAME(short_name)
#define WIDEN_SHORT_NAME_4(short_name) \
  WIDEN_SHORT_NAME(WIDEN_SHORT_NAME(short_name))
#define WIDEN_SHORT_NAME_8(short_name) \
  WIDEN_SHORT_NAME(WIDEN_SHORT_NAME(WIDEN_SHORT_NAME(short_name)))
#define WIDEN_SHORT_NAME_N(n, short_name) WIDEN_SHORT_NAME_##n(short_name)

#define WIDEN_LMUL_mf8 mf4
#define WIDEN_LMUL_mf4 mf2
#define WIDEN_LMUL_mf2 m1
#define WIDEN_LMUL_m1 m2
#define WIDEN_LMUL_m2 m4
#define WIDEN_LMUL_m4 m8

#define WIDEN_LMUL0(lmul) WIDEN_LMUL_##lmul
#define WIDEN_LMUL(...) WIDEN_LMUL0(__VA_ARGS__)

#define WIDEN_LMUL_2(short_name) WIDEN_LMUL(short_name)
#define WIDEN_LMUL_4(short_name) WIDEN_LMUL(WIDEN_LMUL(short_name))
#define WIDEN_LMUL_8(short_name) WIDEN_LMUL(WIDEN_LMUL(WIDEN_LMUL(short_name)))
#define WIDEN_LMUL_N(n, short_name) WIDEN_LMUL_##n(short_name)

#define WIDEN_VREG_NAME(short_name, lmul) \
  VREG_NAME(WIDEN_SHORT_NAME(short_name), WIDEN_LMUL(lmul))

#define WIDEN_VREG_NAME_N(n, short_name, lmul) \
  VREG_NAME(WIDEN_SHORT_NAME_N(n, short_name), WIDEN_LMUL_N(n, lmul))

#define TO_UNSIGNED_i8 u8
#define TO_UNSIGNED_i16 u16
#define TO_UNSIGNED_i32 u32
#define TO_UNSIGNED_i64 u64
#define TO_UNSIGNED_u8 u8
#define TO_UNSIGNED_u16 u16
#define TO_UNSIGNED_u32 u32
#define TO_UNSIGNED_u64 u64

#define TO_UNSIGNED0(lmul) TO_UNSIGNED_##lmul
#define TO_UNSIGNED(...) TO_UNSIGNED0(__VA_ARGS__)

#define UNSIGNED_VREG_NAME(short_name, lmul) \
  VREG_NAME(TO_UNSIGNED(short_name), lmul)

#define VV_OP_TEST(name, ratio, short_name, lmul)                              \
  OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));

#define VX_OP_TEST(name, ratio, short_name, lmul)                              \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (C_TYPE_NAME(short_name), rs1), (rvv::vl_t<ratio>, vl));

#define BIN_OP_TEST(name, ratio, short_name, lmul) \
  VV_OP_TEST(name, ratio, short_name, lmul)        \
  VX_OP_TEST(name, ratio, short_name, lmul)

#define UNARY_OP_TEST(name, ratio, short_name, lmul)                           \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (rvv::vl_t<ratio>, vl));

#define UNARY_OP_TEST_NO_MASK(name, ratio, short_name, lmul)               \
  OP_TEST_NO_MASK(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  VREG_NAME(short_name, lmul),                             \
                  (VREG_NAME(short_name, lmul), vs2), (rvv::vl_t<ratio>, vl));

#define WIDENING_VV_OP_TEST(name, ratio, short_name, lmul)             \
  OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                       \
              (VREG_NAME(short_name, lmul), vs2),                      \
              (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define WIDENING_VX_OP_TEST(name, ratio, short_name, lmul)             \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                       \
              (VREG_NAME(short_name, lmul), vs2),                      \
              (C_TYPE_NAME(short_name), vs1), (rvv::vl_t<ratio>, vl));
#define WIDENING_WV_OP_TEST(name, ratio, short_name, lmul)             \
  OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                       \
              (WIDEN_VREG_NAME(short_name, lmul), vs2),                \
              (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));
#define WIDENING_WX_OP_TEST(name, ratio, short_name, lmul)             \
  OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
              WIDEN_VREG_NAME(short_name, lmul),                       \
              (WIDEN_VREG_NAME(short_name, lmul), vs2),                \
              (C_TYPE_NAME(short_name), vs1), (rvv::vl_t<ratio>, vl));
#define WIDENING_OP_TEST(name, ratio, short_name, lmul) \
  WIDENING_VV_OP_TEST(name, ratio, short_name, lmul)    \
  WIDENING_VX_OP_TEST(name, ratio, short_name, lmul)    \
  WIDENING_WV_OP_TEST(name, ratio, short_name, lmul)    \
  WIDENING_WX_OP_TEST(name, ratio, short_name, lmul)

#define FMA_OP_TEST_TU(name, rvv_name, mask_type, ret_type, ...)    \
  ret_type name##_tu(FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) {        \
    return rvv::tu::rvv_name(FOR_EACH_LIST(ARG_NAME, __VA_ARGS__)); \
  }
#define FMA_OP_TEST_TUM(name, rvv_name, mask_type, ret_type, ...)           \
  ret_type name##_tum(mask_type vm, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::tu::rvv_name(vm, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));     \
  }
#define FMA_OP_TEST_MU(name, rvv_name, mask_type, ret_type, ...)           \
  ret_type name##_mu(mask_type vm, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::mu::rvv_name(vm, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));    \
  }
#define FMA_OP_TEST_TUMU(name, rvv_name, mask_type, ret_type, ...)           \
  ret_type name##_tumu(mask_type vm, FOR_EACH_LIST(ARG_PAIR, __VA_ARGS__)) { \
    return rvv::tumu::rvv_name(vm, FOR_EACH_LIST(ARG_NAME, __VA_ARGS__));    \
  }

#define FMA_OP_TEST_ALL(name, rvv_name, mask_type, ret_type, ...)   \
  OP_TEST(name, rvv_name, mask_type, ret_type, __VA_ARGS__)         \
  OP_TEST_M(name, rvv_name, mask_type, ret_type, __VA_ARGS__)       \
  FMA_OP_TEST_TU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)  \
  FMA_OP_TEST_TUM(name, rvv_name, mask_type, ret_type, __VA_ARGS__) \
  FMA_OP_TEST_MU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)  \
  FMA_OP_TEST_TUMU(name, rvv_name, mask_type, ret_type, __VA_ARGS__)

#define FMA_VV_OP_TEST(name, ratio, short_name, lmul)                      \
  FMA_OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  VREG_NAME(short_name, lmul),                             \
                  (VREG_NAME(short_name, lmul), vd),                       \
                  (VREG_NAME(short_name, lmul), vs2),                      \
                  (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));

#define FMA_VX_OP_TEST(name, ratio, short_name, lmul)                      \
  FMA_OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  VREG_NAME(short_name, lmul),                             \
                  (VREG_NAME(short_name, lmul), vd),                       \
                  (C_TYPE_NAME(short_name), rs1),                          \
                  (VREG_NAME(short_name, lmul), vs2), (rvv::vl_t<ratio>, vl));

#define FMA_OP_TEST(name, ratio, short_name, lmul) \
  FMA_VV_OP_TEST(name, ratio, short_name, lmul)    \
  FMA_VX_OP_TEST(name, ratio, short_name, lmul)

#define VXM_V_TEST(name, ratio, short_name, lmul)                            \
  OP_TEST_NO_MASK(name##_vxm_##short_name##lmul, name, rvv::vmask_t<ratio>,  \
                  VREG_NAME(short_name, lmul),                               \
                  (VREG_NAME(short_name, lmul), vs2),                        \
                  (C_TYPE_NAME(short_name), rs1), (rvv::vmask_t<ratio>, v0), \
                  (rvv::vl_t<ratio>, vl));
#define VVM_V_TEST(name, ratio, short_name, lmul)                           \
  OP_TEST_NO_MASK(name##_vxm_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  VREG_NAME(short_name, lmul),                              \
                  (VREG_NAME(short_name, lmul), vs2),                       \
                  (VREG_NAME(short_name, lmul), vs1),                       \
                  (rvv::vmask_t<ratio>, v0), (rvv::vl_t<ratio>, vl));

#define CALLABLE_VV_OP_TEST(name, func, ratio, short_name, lmul)               \
  OP_TEST_ALL(name##_vv_##short_name##lmul, func, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));

#define CALLABLE_VX_OP_TEST(name, func, ratio, short_name, lmul)               \
  OP_TEST_ALL(name##_vx_##short_name##lmul, func, rvv::vmask_t<ratio>,         \
              VREG_NAME(short_name, lmul), (VREG_NAME(short_name, lmul), vs2), \
              (C_TYPE_NAME(short_name), rs1), (rvv::vl_t<ratio>, vl));

#define CALLABLE_BIN_OP_TEST(name, func, ratio, short_name, lmul) \
  CALLABLE_VV_OP_TEST(name, func, ratio, short_name, lmul)        \
  CALLABLE_VX_OP_TEST(name, func, ratio, short_name, lmul)

#define WIDENING_FMA_VV_OP_TEST(name, ratio, short_name, lmul)             \
  FMA_OP_TEST_ALL(name##_vv_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  WIDEN_VREG_NAME(short_name, lmul),                       \
                  (WIDEN_VREG_NAME(short_name, lmul), vd),                 \
                  (VREG_NAME(short_name, lmul), vs2),                      \
                  (VREG_NAME(short_name, lmul), vs1), (rvv::vl_t<ratio>, vl));

#define WIDENING_FMA_VX_OP_TEST(name, ratio, short_name, lmul)             \
  FMA_OP_TEST_ALL(name##_vx_##short_name##lmul, name, rvv::vmask_t<ratio>, \
                  WIDEN_VREG_NAME(short_name, lmul),                       \
                  (WIDEN_VREG_NAME(short_name, lmul), vd),                 \
                  (C_TYPE_NAME(short_name), rs1),                          \
                  (VREG_NAME(short_name, lmul), vs2), (rvv::vl_t<ratio>, vl));

#endif  // MACROS_H_
