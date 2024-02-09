#ifndef MACROS_TYPE_H_
#define MACROS_TYPE_H_

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
#endif  // MACROS_TYPE_H_
