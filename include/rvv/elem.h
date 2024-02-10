// Copyright (c) 2024 <Sirui Lu (siruilu@cs.washington.edu)>
#ifndef RVV_ELEM_H_
#define RVV_ELEM_H_

#include <rvv/config.h>
#include <stddef.h>
#include <stdint.h>

#include <type_traits>

namespace rvv {
template <typename E, typename... Es>
concept AnyOf = (... || std::is_same_v<E, Es>);

#if HAS_FLOAT16
template <typename E>
concept IsFloat16 = std::is_same_v<E, float16_t>;
#endif

template <typename E>
concept IsFloat32 = std::is_same_v<E, float>;

template <typename E>
concept IsFloat64 = std::is_same_v<E, double>;

template <typename E>
concept IsFloatingPoint =
#if HAS_FLOAT16
    IsFloat16<E> ||
#endif
    IsFloat32<E> || IsFloat64<E>;

template <typename E>
concept IsUnsigned = AnyOf<E, uint8_t, uint16_t, uint32_t, uint64_t>;

template <typename E>
concept IsSigned = AnyOf<E, int8_t, int16_t, int32_t, int64_t>;

template <typename E>
concept IsIntegral = IsSigned<E> || IsUnsigned<E>;

template <typename E>
concept IsElement = IsSigned<E> || IsUnsigned<E> || IsFloatingPoint<E>;

template <typename E, bool kNeedZvfh>
concept NeedUnsupportedZvfh =
#if HAS_ZVFH
    false;
#elif HAS_ZVFHMIN
    kNeedZvfh;
#elif HAS_FLOAT16
    std::is_same_v<E, _Float16>;
#else
    false;
#endif

template <typename E>
concept NeedUnsupportedZve32f =
#if HAS_ZVE32F
    false;
#else
    std::is_same_v<E, float>;
#endif

template <typename E>
concept NeedUnsupportedZve64d =
#if HAS_ZVE64D
    false;
#else
    std::is_same_v<E, double>;
#endif

template <typename E>
concept NeedUnsupportedZve64x =
#if HAS_ZVE64X
    false;
#else
    AnyOf<E, int64_t, uint64_t>;
#endif

template <typename E>
concept SupportedIntegralElement = !NeedUnsupportedZve64x<E> && IsIntegral<E>;

template <typename E>
concept SupportedSignedElement = SupportedIntegralElement<E> && IsSigned<E>;

template <typename E>
concept SupportedUnsignedElement = SupportedIntegralElement<E> && IsUnsigned<E>;

template <typename E, bool kNeedZvfh>
concept SupportedFloatingPointElement =
    !NeedUnsupportedZvfh<E, kNeedZvfh> && !NeedUnsupportedZve32f<E> &&
    !NeedUnsupportedZve64d<E> && IsFloatingPoint<E>;

template <typename E, bool kNeedZvfh>
concept SupportedElement =
    SupportedIntegralElement<E> || SupportedFloatingPointElement<E, kNeedZvfh>;

namespace internal {
template <size_t kBits>
struct UnsignedType {
  using Type = void;
};

template <>
struct UnsignedType<8> {
  using Type = uint8_t;
};

template <>
struct UnsignedType<16> {
  using Type = uint16_t;
};

template <>
struct UnsignedType<32> {
  using Type = uint32_t;
};

template <>
struct UnsignedType<64> {
  using Type = uint64_t;
};

template <size_t kBits>
struct SignedType {
  using Type = void;
};

template <>
struct SignedType<8> {
  using Type = int8_t;
};

template <>
struct SignedType<16> {
  using Type = int16_t;
};

template <>
struct SignedType<32> {
  using Type = int32_t;
};

template <>
struct SignedType<64> {
  using Type = int64_t;
};

template <size_t kBits>
struct FloatingPointType {
  using Type = void;
};

template <>
struct FloatingPointType<16> {
  using Type = float16_t;
};

template <>
struct FloatingPointType<32> {
  using Type = float32_t;
};

template <>
struct FloatingPointType<64> {
  using Type = float64_t;
};
}  // namespace internal

template <size_t kBits>
  requires SupportedUnsignedElement<
               typename internal::UnsignedType<kBits>::Type>
using uint_t = typename internal::UnsignedType<kBits>::Type;

template <size_t kBits>
  requires SupportedSignedElement<typename internal::SignedType<kBits>::Type>
using int_t = typename internal::SignedType<kBits>::Type;

template <size_t kBits>
  requires SupportedFloatingPointElement<
               typename internal::FloatingPointType<kBits>::Type, false>
using float_t = typename internal::FloatingPointType<kBits>::Type;

}  // namespace rvv

#endif  // RVV_ELEM_H_
